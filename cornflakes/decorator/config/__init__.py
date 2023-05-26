"""cornflakes config decorator module."""
from cornflakes.decorator.config._config import config
from cornflakes.decorator.config._config_group import config_group
from cornflakes.decorator.dataclass.helper import config_files, dataclass_fields, is_config

__all__ = ["config", "config_group", "is_config", "config_files", "dataclass_fields"]
