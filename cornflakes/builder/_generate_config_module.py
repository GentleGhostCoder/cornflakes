"""cornflakes config generation."""
from dataclasses import is_dataclass
import importlib
import inspect
import logging
import os
import sysconfig
from types import ModuleType
from typing import Dict, List, Optional, Union

import cornflakes.builder.config_template
from cornflakes.common import unquoted_string
from cornflakes.decorator import ConfigArguments, Loader, field
from cornflakes.decorator.config import config_files, config_group, is_config


def generate_group_module(  # noqa: C901
    source_module: Union[ModuleType, str],
    source_config: Optional[Union[Dict[str, Union[List[str], str]], List[str], str]] = None,
    target_module_file: Optional[str] = None,
    class_name: Optional[str] = None,
    loader: Loader = Loader.FILE_LOADER,
    *args,
    **kwargs,
):
    """Module with function to generate automatically config group module."""
    declaration = []
    ini_config_objects = {}
    imports = []
    extra_imports = []
    files = kwargs.get(ConfigArguments.files.name, [])
    files = files if isinstance(files, list) else [files]

    if ConfigArguments.files.name not in kwargs:
        kwargs.update({ConfigArguments.files.name: source_config})

    if not target_module_file:
        target_module_file = f'{source_module.__name__.replace(".", "/")}/default.py'

    with open(cornflakes.builder.config_template.__file__) as file:
        template = file.read()

    if class_name:
        template = template.replace("class Config", f"class {class_name}")
        template = template.replace('["Config"]', f'["{class_name}"]')

    # Write Template to prevent import errors
    with open(target_module_file, "w") as file:
        file.write(template)

    if isinstance(source_module, str):
        source_module = importlib.import_module(source_module)

    for cfg_name, cfg_class in inspect.getmembers(source_module):
        if is_dataclass(cfg_class) and inspect.isclass(cfg_class) and is_config(cfg_class):
            cfg = getattr(cfg_class, str(loader.value))(files=source_config)
            ini_config_objects.update(cfg)
            imports.append(cfg_name)
            files.extend([file for file in config_files(cfg_class) if file and file not in files])

    if ConfigArguments.filter_function.name in kwargs:
        filter_function = kwargs.pop(ConfigArguments.filter_function.name)
        kwargs[ConfigArguments.filter_function.name] = unquoted_string(filter_function.__name__)
        extra_imports.append(f"from {filter_function.__module__} import {filter_function.__name__}")

    logging.debug(f"Found configs: {imports}")

    declaration.extend(
        [
            (
                f"{cfg_name}: List[{cfg[0].__class__.__name__}] = "
                f"{field.__name__}(default_factory={cfg.__class__.__name__})"
                if isinstance(cfg, list)
                else f"{cfg_name}: {cfg.__class__.__name__} = {cfg.__class__.__name__}()"
            )
            for cfg_name, cfg in ini_config_objects.items()
        ]
    )

    extra_imports.extend(
        [f"from {field.__module__} import {field.__name__}", "from typing import List"] if declaration else []
    )

    if args or kwargs:
        kwargs.update({key: repr(value).replace("'", '"') for key, value in kwargs.items()})
        template = template.replace(
            f"@{config_group.__name__}",
            (
                f"@{config_group.__name__}("
                f"{', '.join([*args, *[f'{key}={value}' for key, value in kwargs.items()]])})"
            ),
        )

    template = template.replace(
        "from",
        (
            f"""{'''
'''.join(extra_imports)}\n\nfrom {source_module.__name__} import {
            ''', '''.join(imports)}\nfrom"""
        ),
    )
    template = template.replace(
        "# modules",
        f"""{'''
    '''.join(declaration)}""",
        1,
    )

    with open(target_module_file, "w") as file:
        file.write(template)

    if "black" in os.listdir(sysconfig.get_paths()["purelib"]):
        # fix format
        # source_config = " ".join(source_config) if isinstance(source_config, list) else source_config
        os.system(f"black {target_module_file}")  # noqa: S605
    if "isort" in os.listdir(sysconfig.get_paths()["purelib"]):
        os.system(f"isort {target_module_file}")  # noqa: S605
