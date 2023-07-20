"""cornflakes decorator module."""  # noqa: RST303 D205

from cornflakes.decorator._funcat import funcat
from cornflakes.decorator._indexer import Index
from cornflakes.decorator._wrap_kwargs import wrap_kwargs
from cornflakes.decorator.click import click_cli
from cornflakes.decorator.dataclasses import dataclass, field, config, config_group
from cornflakes.decorator.string_builder import string_builder


__all__ = [
    "click_cli",
    "config",
    "config_group",
    "dataclass",
    "field",
    "config",
    "config_group",
    "Index",
    "funcat",
    "wrap_kwargs",
    "string_builder",
]
