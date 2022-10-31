"""cornflakes config decorator module."""
from cornflakes.decorator.config._config import config, Config
from cornflakes.decorator.config._config_group import config_group, ConfigGroup
from cornflakes.decorator.config._loader import Loader
from cornflakes.decorator.config._helper import is_config


__all__ = [
    "config",
    "config_group",
    "is_config",
    "Config",
    "ConfigGroup",
    "Loader",
]
