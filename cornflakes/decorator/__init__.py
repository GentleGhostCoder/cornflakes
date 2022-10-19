"""cornflakes decorator module.
__________________________________

.. currentmodule:: cornflakes.decorator

.. autosummary::
   :toctree: _generate

    ini_config
"""  # noqa: RST303 D205
from cornflakes.decorator._ini_config import ini_config, ini_group

__all__ = ["ini_config", "ini_group"]
