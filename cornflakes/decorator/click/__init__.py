"""Click Extension for better CLI.
__________________________________
See referenced Code at https://github.com/ewels/rich-click.git
"""  # noqa: RST303 D205
from cornflakes.decorator.click._click_cli import click_cli
from cornflakes.decorator.click.rich import RichArg, argument, RichCommand, command, RichGroup, group, RichConfig
from cornflakes.decorator.click.options import bg_process_option, verbose_option, global_option, auto_option


__all__ = [
    "global_option",
    "verbose_option",
    "bg_process_option",
    "auto_option",
    "group",
    "command",
    "argument",
    "RichArg",
    "RichGroup",
    "RichCommand",
    "RichConfig",
    "click_cli",
]
