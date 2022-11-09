"""cornflakes.click.rich Module."""
from click import group as click_group
from click import command as click_command
from click import argument as click_argument
from cornflakes.click.rich._rich_config import RichConfig
from cornflakes.click.rich._rich_group import RichGroup
from cornflakes.click.rich._rich_argument import RichArg
from cornflakes.click.rich._rich_global_option_wrapper import rich_global_option_wrapper
from typing import Callable, Union

from cornflakes.click.rich._rich_command import RichCommand

F = Callable[..., Union[RichCommand, RichGroup, RichArg]]


def group(*args, cls=RichGroup, **kwargs) -> F:  # type: ignore
    """Group decorator function.

    Defines the group() function so that it uses the RichGroup class by default.
    """
    return rich_global_option_wrapper(click_group, *args, cls=cls, **kwargs)


def command(*args, cls=RichCommand, **kwargs) -> F:  # type: ignore
    """Command decorator function.

    Defines the command() function so that it uses the RichCommand class by default.
    """
    return rich_global_option_wrapper(click_command, *args, cls=cls, **kwargs)


def argument(*args, cls=RichArg, **kwargs) -> F:  # type: ignore
    """Command decorator function.

    Defines the command() function so that it uses the RichCommand class by default.
    """
    return click_argument(*args, cls=cls, **kwargs)


__all__ = ["RichConfig", "RichGroup", "RichCommand", "RichArg", "command", "group", "argument"]
