"""cornflakes decorator module.
__________________________________

.. currentmodule:: cornflakes.decorator

.. autosummary::
   :toctree: _generate

    config
    config_group
    config_field
    add_slots
    click_cli
"""  # noqa: RST303 D205
from cornflakes.decorator.config import config, config_group, Loader, config_field
from cornflakes.decorator._add_dataclass_slots import add_slots
from cornflakes.decorator._click_cli import click_cli
from cornflakes.decorator.dataclass import field, dataclass


__all__ = ["config", "config_group", "config_field", "add_slots", "click_cli", "dataclass", "field", "Loader"]
