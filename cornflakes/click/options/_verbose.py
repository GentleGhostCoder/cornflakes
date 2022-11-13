import logging

from cornflakes.click.options._global import global_option
from cornflakes.logging import setup_logging


@global_option(
    ["-v", "--verbose"],
    is_flag=True,
    help="Base logging level is set to logging.DEBUG.",
)
def verbose_option(verbose):
    """Default Option for verbose logging."""
    setup_logging(default_level=logging.DEBUG if verbose else None, force=True)
