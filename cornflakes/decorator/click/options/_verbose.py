import logging

from cornflakes.decorator.click.options._global import global_option
from cornflakes.logging.logger import setup_logging


@global_option(
    ["-v", "--verbose"],
    help="Base logging level is set to logging.DEBUG.",
    # option_group="Basic Options",
    is_flag=True,
)
def verbose_option(verbose, self):
    """Default Option for verbose logging."""
    loggers = []
    if self.callback.__module__:
        main_module_name = self.callback.__module__.split(".", 1)[0] if self.callback.__module__ else None
        loggers = [logger for logger in logging.root.manager.loggerDict if main_module_name in logger]
    if hasattr(self, "config") and hasattr(self.config, "VERBOSE_LOGGER") and len(self.config.VERBOSE_LOGGER):
        loggers.extend(self.config.VERBOSE_LOGGER)
    setup_logging(default_level=logging.DEBUG if verbose else logging.root.level, loggers=loggers)


@global_option(
    ["-vv", "--verbose-all"],
    help="Base logging level is set to logging.DEBUG.",
    # option_group="Basic Options",
    is_flag=True,
)
def verbose_option_all(verbose_all):
    """Default Option for verbose logging."""
    setup_logging(default_level=logging.DEBUG if verbose_all else logging.root.level, force=True)
