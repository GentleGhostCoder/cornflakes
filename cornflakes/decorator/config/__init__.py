"""cornflakes config decorator module."""
from cornflakes.common import patch_module
from cornflakes.decorator.config._config import config, Config
from cornflakes.decorator.config._config_group import config_group, ConfigGroup
from cornflakes.decorator.config._helper import is_config
from cornflakes.decorator.config._helper import config_files

__all__ = ["config", "config_group", "is_config", "Config", "ConfigGroup", "config_files"]

patch_module(globals())
