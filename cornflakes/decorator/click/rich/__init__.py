"""cornflakes.click.rich Module."""
from typing import Callable, Optional, Union, Any

from click import argument as click_argument
from click import option as click_option
from click import command as click_command
from click import group as click_group, Command, Group, BaseCommand, Argument

from cornflakes.decorator.click._fill_option_groups import fill_option_groups
from cornflakes.decorator.click.rich._rich_argument import RichArg
from cornflakes.decorator.click.rich._rich_command import RichCommand
from cornflakes.decorator.click.rich._rich_config import RichConfig
from cornflakes.decorator.click.rich._rich_global_option_wrapper import rich_global_option_wrapper
from cornflakes.decorator.click.rich._rich_group import RichGroup

AnyCallable = Callable[..., Any]


def group(*args, cls=RichGroup, **kwargs) -> Callable[[Union[AnyCallable, RichGroup]], RichGroup]:  # type: ignore
    """Group decorator function.

    Defines the group() function so that it uses the RichGroup class by default.
    """
    return rich_global_option_wrapper(click_group, *args, cls=cls, **kwargs)


def command(
    *args, cls=RichCommand, **kwargs
) -> Callable[[Union[AnyCallable, Command, Group, RichCommand, RichGroup]], RichCommand]:  # type: ignore
    """Command decorator function.

    Defines the command() function so that it uses the RichCommand class by default.
    """
    return rich_global_option_wrapper(click_command, *args, cls=cls, **kwargs)


def argument(*args, cls=RichArg, **kwargs) -> Callable[..., Union[Argument, RichArg]]:  # type: ignore
    """Command decorator function.

    Defines the command() function so that it uses the RichCommand class by default.
    """
    return click_argument(*args, cls=cls, **kwargs)


def option(*args, option_group="", **kwargs) -> Callable[..., Union[Argument, RichArg]]:  # type: ignore
    """Command decorator function.

    Defines the command() function so that it uses the RichCommand class by default.
    """

    def decorator(callback):
        """Decorator function for the decorator."""
        fill_option_groups(callback, option_group, *args)
        return click_option(*args, **kwargs)(callback)

    return decorator


def group_command(self, name: Optional[str], cmd: Optional[Union[BaseCommand, Command, RichCommand]] = None):
    """Decorator to register a RichCommand with this group."""

    def wrapper(callback):
        """Wrapper function for the decorator."""
        new_command = command(name=name, config=self.config)(callback)
        self.add_command(new_command, name)
        return new_command

    return wrapper(cmd) if cmd else wrapper


def group_group(self, name: Optional[str], cmd: Optional[Union[Group, RichGroup]] = None):
    """Decorator to register a RichGroup with this group."""

    def wrapper(callback):
        """Wrapper function for the decorator."""
        new_group = group(name=name, config=self.config)(callback)
        self.add_command(new_group, name)
        return new_group

    return wrapper(cmd) if cmd else wrapper


__all__ = [
    "RichConfig",
    "RichGroup",
    "RichCommand",
    "RichArg",
    "command",
    "group",
    "option",
    "argument",
    "group_group",
    "group_command",
]
