"""cornflakes config generation."""

import inspect
import os
import sysconfig
import cornflakes.config._config_template
from cornflakes.logging import logger


def generate_config_group(cfg_module, template_cfg: str = None, target: str = None, name: str = None, *args, **kwargs):
    """Module with function to generate automatically config group module."""
    if not target:
        target = f'{cfg_module.__name__.replace(".", "/")}/default.py'

    logger.debug(f"{cfg_module.__name__} members: {inspect.getmembers(cfg_module)}")

    ini_config_objects = {}
    imports = []
    for cls_name, cls in inspect.getmembers(cfg_module):
        if inspect.isclass(cls) and hasattr(cls, "from_ini") and hasattr(cls, "__ini_config_sections__"):
            ini_config_objects.update(cls.from_ini(template_cfg))
            imports.append(cls_name)

    logger.debug(f"Found configs: {imports}")

    with open(cornflakes.config._config_template.__file__) as file:
        template = file.read()
        template = template.replace(
            "# import config",
            f"""from {cfg_module.__name__} import (
    {''',
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
        if name:
            template = template.replace("class Config", f"class {name}")
            template = template.replace('["Config"]', f'["{name}"]')
        if args or kwargs:
            template = template.replace(
                "@ini_group",
                f"@ini_group({', '.join([*args, *[f'{key}={repr(value)}' for key, value in kwargs.items()]])})",
            )

    with open(target, "w") as file:
        file.write(template)

    if "black" in os.listdir(sysconfig.get_paths()["purelib"]):
        # fix format
        os.system(f"black {template_cfg} {target}")  # noqa: S605


__all__ = ["generate_config_group"]
