"""cornflakes.click.rich Module."""
from typing import Callable, Any, Optional, Union

from click import argument as click_argument
from click import command as click_command
from click import group as click_group, Command, Group

from cornflakes.decorator.click.rich._rich_argument import RichArg
from cornflakes.decorator.click.rich._rich_command import RichCommand
from cornflakes.decorator.click.rich._rich_config import RichConfig
from cornflakes.decorator.click.rich._rich_global_option_wrapper import rich_global_option_wrapper
from cornflakes.decorator.click.rich._rich_group import RichGroup

F = Callable[..., Union[RichCommand, RichGroup, RichArg, Any]]


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


def group_command(self, name: Optional[str], cmd: Union[Command, RichCommand, Any] = None):
    """Decorator to register a RichCommand with this group."""

    def wrapper(callback):
        """Wrapper function for the decorator."""
        new_command = command(name=name, config=self.config)(callback)
        self.add_command(new_command, name)
        return new_command

    if cmd:
        return wrapper(cmd)
    return wrapper


def group_group(self, name: Optional[str], cmd: Union[Group, RichGroup, Any] = None):
    """Decorator to register a RichGroup with this group."""

    def wrapper(callback):
        """Wrapper function for the decorator."""
        new_group = group(name=name, config=self.config)(callback)
        self.add_command(new_group, name)
        return new_group

    if cmd:
        return wrapper(cmd)
    return wrapper


__all__ = ["RichConfig", "RichGroup", "RichCommand", "RichArg", "command", "group", "argument", "group_command"]
