"""cornflakes decorator module.
__________________________________

.. currentmodule:: cornflakes.decorator

.. autosummary::
   :toctree: _generate

    ini_config
"""  # noqa: RST303 D205
from cornflakes.decorator.config import config, config_group
from cornflakes.decorator._add_dataclass_slots import add_slots


__all__ = ["config", "config_group", "add_slots"]
