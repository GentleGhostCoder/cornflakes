"""cornflakes config decorator module."""
from cornflakes.decorator.config._config import config
from cornflakes.decorator.config._config_group import config_group
from cornflakes.decorator.dataclass.helper import is_config, dataclass_fields
from cornflakes.decorator.dataclass.helper import config_files

__all__ = ["config", "config_group", "is_config", "config_files", "dataclass_fields"]
