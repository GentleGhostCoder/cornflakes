"""Default Global Click Options."""
from cornflakes.click.options._bg_process import bg_process_option
from cornflakes.click.options._verbose import verbose_option
from cornflakes.click.options._global import global_option
from cornflakes.click.options._auto_option import auto_option

__all__ = ["verbose_option", "bg_process_option", "global_option", "auto_option"]
