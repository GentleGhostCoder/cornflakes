import inspect
import os

import cornflakes.config._default_config_template


def generate_default_config_py(cfg_class, cfg: str = "", target: str = ""):
    """Function that auto generates default config module from cfg_classes and default-ini-config."""
    if not os.path.exists(cfg) and hasattr(cfg_class, "default"):
        with open(cfg, "w") as file:
            file.write(cfg_class.default.crate_htw_logger_config().to_ini())

    config = {}
    config_list = []
    for cls_name, cls in inspect.getmembers(cfg_class):
        if inspect.isclass(cls) and cls_name != "default":
            config.update(cls.from_ini(cfg).popitem()[1])
            config_list.append(cls_name)
    with open(cornflakes.config._default_config_template.__file__) as file:
        template = (
            file.read()
            .replace(
                "# import config",
                f"""import (
    {''',
    '''.join(config_list)}
    )""",
            )
            .replace(
                "pass",
                f"""{'''
    '''.join([f'{cfg_name}: {cfg.__class__.__name__} = None' for cfg_name, cfg in config.items()])}""",
                1,
            )
            .replace("pass", f"return Config(**{config})")
        )
    with open(target, "w") as file:
        file.write(template)
