"""Click Extension for better CLI.
__________________________________
See referenced Code at https://github.com/ewels/rich-click.git
"""  # noqa: RST303 D205

# from click import *  # noqa: F401, F403
import click

from cornflakes.common import patch_module
from cornflakes.click.rich import RichArg, argument, RichCommand, command, RichGroup, group, RichConfig
from cornflakes.click.options import bg_process_option, verbose_option, global_option, auto_option

# Pach click
click.argument = argument
click.group = group
click.command = command
click.Group = RichGroup
click.Command = RichCommand
click.Argument = RichArg

__all__ = [
    "global_option",
    "verbose_option",
    "bg_process_option",
    "auto_option",
    "group",
    "command",
    "argument",
    "RichGroup",
    "RichCommand",
    "RichConfig",
]

patch_module(globals())
