"""cornflakes config generation."""
from dataclasses import is_dataclass
from importlib import import_module
import inspect
import logging
import os
import sysconfig
from types import ModuleType
from typing import Dict, List, Optional, Union

# from cornflakes.decorator import wrap_kwargs
from cornflakes.decorator.dataclasses import config_files, config_group, field, is_config
from cornflakes.types import Constants, Loader

logger = logging.getLogger(__name__)

DECORATOR_MODULE_NAME = import_module("cornflakes.decorator").__name__
TEMPLATE = f'''"""Template Module."""
from {DECORATOR_MODULE_NAME} import config_group


@config_group
class Config:
    """Template Class."""

    # modules


__all__ = ["Config"]
'''


# @wrap_kwargs(config_group)
def generate_config_group_module(  # noqa: C901
    source_module: Union[ModuleType, str],
    source_config: Optional[Union[Dict[str, Union[List[str], str]], List[str], str]] = None,
    target_module_file: Optional[str] = None,
    class_name: Optional[str] = None,
    loader: Loader = Loader.FILE,
    module_description: str = "Automatically generated Default Config.",
    class_description: str = "Main config class of the module.",
    *args,
    **kwargs,
):
    """Module with function to generate automatically config group module."""
    os.environ["CORNFLAKES_GENERATING_CONFIG_MODULE"] = "True"
    declaration = []
    ini_config_objects = {}
    imports = []
    extra_imports = []
    files = kwargs.get(Constants.config_decorator_args.FILES, [])
    files = files if isinstance(files, list) else [files]

    if Constants.config_decorator_args.FILES not in kwargs:
        kwargs.update({Constants.config_decorator_args.FILES: source_config})

    template = TEMPLATE  # create copy of template

    if class_name:
        template = template.replace("Config", class_name)

    template = template.replace("Template Module.", module_description)
    template = template.replace("Template Class.", class_description)

    if isinstance(source_module, str):
        source_module = import_module(source_module)

    if not target_module_file:
        target_module_file = f'{source_module.__name__.replace(".", "/")}/default.py'

    # Write Template to prevent import errors
    with open(target_module_file, "w") as file:
        file.write(template)

    for cfg_name, cfg_class in inspect.getmembers(source_module):
        if is_dataclass(cfg_class) and inspect.isclass(cfg_class) and is_config(cfg_class):
            cfg = getattr(cfg_class, str(loader.value))(files=source_config)
            ini_config_objects.update(cfg)
            imports.append(cfg_name)
            files.extend([file for file in config_files(cfg_class) if file and file not in files])

    logger.debug(f"Found configs: {imports}")
    declaration.extend(
        [
            (
                f"{cfg_name}: List[{cfg[0].__class__.__name__}] = "
                f"{field.__name__}(default_factory={cfg.__class__.__name__})"
                if isinstance(cfg, list)
                else f"{cfg_name}: {cfg.__class__.__name__} = {field.__name__}(default_factory={cfg.__class__.__name__})"
            )
            for cfg_name, cfg in ini_config_objects.items()
        ]
    )

    extra_imports.extend(
        [f"from {DECORATOR_MODULE_NAME} import {field.__name__}", "from typing import List"] if declaration else []
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

    if os.path.exists(sysconfig.get_paths()["purelib"]):
        if "black" in os.listdir(sysconfig.get_paths()["purelib"]):
            # fix format
            # source_config = " ".join(source_config) if isinstance(source_config, list) else source_config
            os.system(f"black {target_module_file}")  # noqa: S605
        if "isort" in os.listdir(sysconfig.get_paths()["purelib"]):
            os.system(f"isort {target_module_file}")  # noqa: S605
