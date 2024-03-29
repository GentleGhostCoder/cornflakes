"""Default Global Click Options."""
from cornflakes.decorator.click.options._config_option import config_option
from cornflakes.decorator.click.options._bg_process import bg_process_option
from cornflakes.decorator.click.options._global import global_option
from cornflakes.decorator.click.options._verbose import verbose_option

__all__ = [
    "verbose_option",
    "bg_process_option",
    "global_option",
    "config_option",
]
