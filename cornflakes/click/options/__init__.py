"""Default Global Click Options."""
from cornflakes.click.options._bg_process import bg_process_option
from cornflakes.click.options._verbose import verbose_option
from cornflakes.click.options._global import global_option
from cornflakes.click.options._version import version_option

__all__ = ["verbose_option", "bg_process_option", "global_option", "version_option"]
