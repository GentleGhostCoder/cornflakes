"""cornflakes config generation."""

import inspect
import os
import sysconfig
from typing import Union, List, Dict

import cornflakes.config._config_template
from cornflakes.common import import_component
from cornflakes.logging import logger


def generate_ini_group_module(
    source_module,
    source_files: Union[str, List[str], Dict[str, Union[str, List[str]]]] = None,
    target_module_file: str = None,
    class_name: str = None,
    *args,
    **kwargs,
):
    """Module with function to generate automatically config group module."""
    if not target_module_file:
        target_module_file = f'{source_module.__name__.replace(".", "/")}/default.py'

    with open(cornflakes.config._config_template.__file__) as file:
        template = file.read()

    if class_name:
        template = template.replace("class Config", f"class {class_name}")
        template = template.replace('["Config"]', f'["{class_name}"]')
    if args or kwargs:
        template = template.replace(
            "@ini_group",
            f"@ini_group({', '.join([*args, *[f'{key}={repr(value)}' for key, value in kwargs.items()]])})",
        )

    # Write Template to prevent import errors
    with open(target_module_file, "w") as file:
        file.write(template)

    if isinstance(source_module, str):
        source_module = import_component(source_module)

    logger.debug(f"{source_module.__name__} members: {inspect.getmembers(source_module)}")

    ini_config_objects = {}
    imports = []
    for cls_name, cls in inspect.getmembers(source_module):
        if inspect.isclass(cls) and hasattr(cls, "from_ini") and hasattr(cls, "__ini_config_sections__"):
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


__all__ = ["generate_ini_group_module"]
