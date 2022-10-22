"""cornflakes Logger.
__________________________________

.. currentmodule:: cornflakes.logging

.. autosummary::
   :toctree: _generate

    logger
    LoggerInterface
    attach_log
"""  # noqa: RST303 D205
from cornflakes.logging._logger import LoggerInterface, attach_log, logger

__all__ = ["LoggerInterface", "attach_log", "logger"]
