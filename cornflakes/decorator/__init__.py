"""cornflakes decorator module."""  # noqa: RST303 D205

from cornflakes.decorator._add_dataclass_slots import add_slots
from cornflakes.decorator._funcat import funcat
from cornflakes.decorator._indexer import Index
from cornflakes.decorator._wrap_kwargs import wrap_kwargs
from cornflakes.decorator.click import click_cli
from cornflakes.decorator.config import config, config_group
from cornflakes.decorator.dataclass import dataclass, field
from cornflakes.decorator.string_builder import string_builder

config_field = field

__all__ = [
    "config",
    "config_group",
    "config_field",
    "add_slots",
    "click_cli",
    "dataclass",
    "field",
    "Index",
    "funcat",
    "wrap_kwargs",
    "string_builder",
]
