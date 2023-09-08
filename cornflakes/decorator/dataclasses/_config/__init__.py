"""cornflakes config decorator module."""
from cornflakes.decorator.dataclasses._config._config import config
from cornflakes.decorator.dataclasses._config._config_group import config_group
from cornflakes.decorator.dataclasses._config._ini import to_ini, to_ini_bytes
from cornflakes.decorator.dataclasses._config._yaml import to_yaml, to_yaml_bytes

__all__ = ["config", "config_group", "to_ini", "to_ini_bytes", "to_yaml", "to_yaml_bytes"]
