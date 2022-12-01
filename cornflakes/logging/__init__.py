"""cornflakes Logger.
__________________________________
"""  # noqa: RST303 D205
from cornflakes.common import patch_module
from cornflakes.logging._logger import attach_log, setup_logging

__all__ = ["attach_log", "setup_logging"]

patch_module(globals())
