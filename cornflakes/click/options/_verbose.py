import logging

from cornflakes.click.options._global import global_option
from cornflakes.logging.logger import setup_logging


@global_option(
    ["-v", "--verbose"],
    help="Base logging level is set to logging.DEBUG.",
    is_flag=True,
)
def verbose_option(verbose):
    """Default Option for verbose logging."""
    setup_logging(default_level=logging.DEBUG if verbose else None)


@global_option(
    ["-vv", "--verbose-all"],
    help="Base logging level is set to logging.DEBUG.",
    is_flag=True,
)
def verbose_option_all(verbose):
    """Default Option for verbose logging."""
    setup_logging(default_level=logging.DEBUG if verbose else None, force=True)
