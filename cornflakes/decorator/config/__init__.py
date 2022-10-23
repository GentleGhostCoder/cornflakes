"""cornflakes config decorator module."""
from cornflakes.decorator.config._config import config
from cornflakes.decorator.config._config_group import config_group
from cornflakes.decorator.config._loader import (
    YAML_LOADER,
    INI_LOADER,
    DICT_LOADER,
    YAML_WRITER,
    INI_WRITER,
    INI_BYTES_PARSER,
    YAML_BYTES_PARSER,
)


def is_config(cls):
    """Methoad to return falg that class is a config class."""
    return hasattr(cls, "__config_sections__")


def is_group(cls):
    """Methoad to return falg that class is a config group class."""
    return not hasattr(cls, "__config_sections__") and hasattr(cls, "__config_files__")


__all__ = [
    "config",
    "config_group",
    "is_config",
    "YAML_LOADER",
    "INI_LOADER",
    "DICT_LOADER",
    "YAML_WRITER",
    "INI_WRITER",
    "INI_BYTES_PARSER",
    "YAML_BYTES_PARSER",
]
