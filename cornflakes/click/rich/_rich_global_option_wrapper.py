from functools import wraps
from inspect import signature
from typing import Callable, Union

from cornflakes.click.rich._rich_argument import RichArg
from cornflakes.click.rich._rich_command import RichCommand
from cornflakes.click.rich._rich_group import RichGroup

F = Callable[..., Union[RichCommand, RichGroup, RichArg]]


def rich_global_option_wrapper(click_func, *wrap_args, **wrap_kwargs) -> F:
    """Wrapper Method for rich command / group."""

    def global_option_click_decorator(func):

        click_cls = click_func(*wrap_args, **wrap_kwargs)(func)

        @wraps(func)
        def click_callback(*args, **kwargs):
            kwargs["self"]: RichGroup = func
            kwargs["parent"]: RichGroup = click_cls
            if click_cls.config:
                if click_cls.config.GLOBAL_OPTIONS and func.__module__ != "cornflakes.click":
                    for option_obj in click_cls.config.GLOBAL_OPTIONS:
                        option_obj(
                            *args,
                            **{
                                key: value
                                for key, value in kwargs.items()
                                if key in signature(option_obj).parameters.keys()
                            },
                        )
            return func(
                *args, **{key: value for key, value in kwargs.items() if key in signature(func).parameters.keys()}
            )

        click_cls.callback = click_callback
        return click_cls

    return global_option_click_decorator
