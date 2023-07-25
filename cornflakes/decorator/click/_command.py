from typing import Any, Callable, Union

from click import Command, Group

from cornflakes.decorator import wrap_kwargs
from cornflakes.decorator.click._click_cli import click_cli
from cornflakes.decorator.click.rich import RichCommand, RichGroup

AnyCallable = Callable[..., Any]


@wrap_kwargs(RichCommand)
@wrap_kwargs(Command)
@wrap_kwargs(click_cli, exclude=["as_command"])
def command(*args, **kwargs) -> Callable[[Union[AnyCallable, Command, Group, RichCommand, RichGroup]], RichCommand]:
    """Command decorator function.

    Defines the command() function so that it uses the RichCommand class by default"""
    kwargs.pop("as_command", None)
    return click_cli(*args, as_command=True, **kwargs)
