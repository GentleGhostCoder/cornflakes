"""cornflakes config generation."""
import inspect
import os
import sysconfig
from types import ModuleType
from typing import Dict, List, Union

import cornflakes.builder.config_template
from cornflakes.common import import_component
from cornflakes.decorator.config import config_group, is_config
from cornflakes.logging import logger


def generate_group_module(
    source_module: Union[ModuleType, str],
    source_files: Union[str, List[str], Dict[str, Union[str, List[str]]]] = None,
    target_module_file: str = None,
    class_name: str = None,
    *args,
    **kwargs,
):
    """Module with function to generate automatically config group module."""
    if not target_module_file:
        target_module_file = f'{source_module.__name__.replace(".", "/")}/default.py'

    with open(cornflakes.builder.config_template.__file__) as file:
        template = file.read()

    if class_name:
        template = template.replace("class Config", f"class {class_name}")
        template = template.replace('["Config"]', f'["{class_name}"]')
    if args or kwargs:
        template = template.replace(
            f"@{config_group.__name__}",
            f"@{config_group.__name__}({', '.join([*args, *[f'{key}={repr(value)}' for key, value in kwargs.items()]])})",
        )

    # Write Template to prevent import errors
    with open(target_module_file, "w") as file:
        file.write(template)

    if isinstance(source_module, str):
        source_module = import_component(source_module)

    ini_config_objects = {}
    imports = []
    for cls_name, cls in inspect.getmembers(source_module):
        if inspect.isclass(cls) and is_config(cls):
            ini_config_objects.update(cls.from_ini(source_files))
            imports.append(cls_name)

    logger.debug(f"Found configs: {imports}")

    template = template.replace(
        "# import config",
        f"""from {source_module.__name__} import ({''',
    '''.join(imports)}
    )""",
    )
    template = template.replace(
        "pass",
        f"""{'''
    '''.join([f'{cfg_name}: {cfg.__class__.__name__} = {cfg.__class__.__name__}()'
              for cfg_name, cfg in ini_config_objects.items()])}""",
        1,
    )

    with open(target_module_file, "w") as file:
        file.write(template)

    if "black" in os.listdir(sysconfig.get_paths()["purelib"]):
        # fix format
        os.system(f"black {source_files} {target_module_file}")  # noqa: S605
