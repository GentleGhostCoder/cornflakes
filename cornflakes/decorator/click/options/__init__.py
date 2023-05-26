"""Default Global Click Options."""
from cornflakes.decorator.click.options._auto_option import auto_option
from cornflakes.decorator.click.options._bg_process import bg_process_option
from cornflakes.decorator.click.options._global import global_option
from cornflakes.decorator.click.options._verbose import verbose_option, verbose_option_all

__all__ = ["verbose_option", "verbose_option_all", "bg_process_option", "global_option", "auto_option"]
