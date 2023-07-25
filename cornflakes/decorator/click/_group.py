from typing import Any, Callable, Union

from click import MultiCommand

from cornflakes.decorator import wrap_kwargs
from cornflakes.decorator.click._click_cli import click_cli
from cornflakes.decorator.click.rich import RichGroup

AnyCallable = Callable[..., Any]


@wrap_kwargs(RichGroup)
@wrap_kwargs(MultiCommand)
@wrap_kwargs(click_cli, exclude=["add_command"])
def group(*args, **kwargs) -> Callable[[Union[AnyCallable, RichGroup]], RichGroup]:
    """Group decorator function.

    Defines the group() function so that it uses the RichGroup class by default."""
    kwargs.pop("as_command", None)
    return click_cli(*args, as_command=False, **kwargs)
