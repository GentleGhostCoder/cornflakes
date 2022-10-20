"""cornflakes decorator module.
__________________________________

.. currentmodule:: cornflakes.decorator

.. autosummary::
   :toctree: _generate

    ini_config
"""  # noqa: RST303 D205
from cornflakes.decorator._ini_config import ini_config, ini_group
from cornflakes.decorator._add_dataclass_slots import add_slots

__all__ = ["ini_config", "ini_group", "add_slots"]
