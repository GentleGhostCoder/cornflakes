"""cornflakes Logger.
__________________________________

.. currentmodule:: cornflakes.logging

.. autosummary::
   :toctree: _generate

    logger
    DefaultLogger
    LoggerInterface
    attach_log
"""  # noqa: RST303 D205
from cornflakes.logging._logger import DefaultLogger, LoggerInterface, attach_log

logger = DefaultLogger

__all__ = ["LoggerInterface", "attach_log", "logger"]
