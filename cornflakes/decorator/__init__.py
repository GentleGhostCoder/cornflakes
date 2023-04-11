"""cornflakes decorator module."""  # noqa: RST303 D205

from cornflakes.decorator._indexer import Index
from cornflakes.decorator._funcat import funcat
from cornflakes.decorator.config import config, config_group
from cornflakes.decorator._add_dataclass_slots import add_slots
from cornflakes.decorator._click_cli import click_cli
from cornflakes.decorator.dataclass import field, dataclass
from cornflakes.decorator._types import ConfigArguments, Loader

config_field = field

__all__ = [
    "config",
    "config_group",
    "config_field",
    "add_slots",
    "click_cli",
    "dataclass",
    "field",
    "Loader",
    "ConfigArguments",
    "Index",
    "funcat",
]
