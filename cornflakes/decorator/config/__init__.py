"""cornflakes config decorator module."""
from cornflakes.decorator.config._config import config
from cornflakes.decorator.config._config_group import config_group


def is_config(cls):
    return hasattr(cls, "__config_sections__")


def is_group(cls):
    return not hasattr(cls, "__config_sections__") and hasattr(cls, "__config_files__")


__all__ = ["config", "config_group"]
