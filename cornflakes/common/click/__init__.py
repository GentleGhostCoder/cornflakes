"""Click Extension for better CLI.

See referenced Code at https://github.com/ewels/rich-click.git
"""
from typing import TYPE_CHECKING

import click
from click import *  # noqa: F401, F403
from click import argument as click_argument
from click import command as click_command
from click import group as click_group

from . import _rich_click  # noqa: F401
from ._rich_argument import RichArg
from ._rich_command import RichCommand
from ._rich_config import Config
from ._rich_group import RichGroup


def group(*args, cls=RichGroup, **kwargs):  # type: ignore
    """Group decorator function.

    Defines the group() function so that it uses the RichGroup class by default.
    """
    return click_group(*args, cls=cls, **kwargs, context_settings=Config.Groups.CONTEXT_SETTINGS)


def command(*args, cls=RichCommand, **kwargs):  # type: ignore
    """Command decorator function.

    Defines the command() function so that it uses the RichCommand class by default.
    """
    return click_command(*args, cls=cls, **kwargs, context_settings=Config.Groups.CONTEXT_SETTINGS)


def argument(*args, cls=RichArg, **kwargs):  # type: ignore
    """Command decorator function.

    Defines the command() function so that it uses the RichCommand class by default.
    """
    return click_argument(*args, cls=cls, **kwargs)


click.Group = RichGroup  # type: ignore
click.Command = RichCommand  # type: ignore

if TYPE_CHECKING:
    from click import Choice, Path, option, version_option, style  # noqa: F401

__all__ = [
    "argument",
    "Choice",
    "option",
    "Path",
    "version_option",
    "group",
    "command",
    "RichGroup",
    "RichCommand",
    "Config",
]
