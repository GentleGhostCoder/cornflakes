"""cornflakes Logger.
__________________________________

.. currentmodule:: cornflakes.logging

.. autosummary::
   :toctree: _generate

    attach_log
    setup_logging
"""  # noqa: RST303 D205
from cornflakes.logging._logger import attach_log, setup_logging

__all__ = ["attach_log", "setup_logging"]
