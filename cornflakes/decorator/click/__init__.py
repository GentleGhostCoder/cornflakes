"""Click Extension for better CLI.
__________________________________
See referenced Code at https://github.com/ewels/rich-click.git
"""  # noqa: RST303 D205
from cornflakes.decorator.click._click_cli import click_cli
from cornflakes.decorator.click._command import command
from cornflakes.decorator.click._group import group
from cornflakes.decorator.click.options import config_option, bg_process_option, global_option, verbose_option
from cornflakes.decorator.click.rich import argument

__all__ = [
    "global_option",
    "verbose_option",
    "bg_process_option",
    "config_option",
    "group",
    "command",
    "argument",
    "click_cli",
]
