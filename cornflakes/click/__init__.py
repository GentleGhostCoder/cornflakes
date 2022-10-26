"""Click Extension for better CLI.
__________________________________
See referenced Code at https://github.com/ewels/rich-click.git

.. currentmodule:: cornflakes.click

.. autosummary::
    :toctree: _generate

    RichArg
    RichCommand
    RichGroup
    RichConfig
    verbose_option
    bg_process_option
"""  # noqa: RST303 D205
from inspect import signature
from typing import Callable, Union, TypeVar
import click
from click import *  # noqa: F401, F403
from click import argument as click_argument
from click import command as click_command
from click import group as click_group

from cornflakes.click._rich_argument import RichArg
from cornflakes.click._rich_command import RichCommand
from cornflakes.click._rich_group import RichGroup
from cornflakes.click._rich_config import Config as RichConfig
from cornflakes.click.options import bg_process_option, verbose_option, global_option, version_option


F = TypeVar("F", bound=Callable[..., Union[RichCommand, RichGroup, RichArg]])


def __rich_global_option_wrapper(click_func, *wrap_args, **wrap_kwargs) -> F:
    def global_option_click_decorator(func):

        click_cls = click_func(*wrap_args, **wrap_kwargs)(func)

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


def group(*args, cls=RichGroup, **kwargs) -> F:  # type: ignore
    """Group decorator function.

    Defines the group() function so that it uses the RichGroup class by default.
    """
    return __rich_global_option_wrapper(click_group, *args, cls=cls, **kwargs)


def command(*args, cls=RichCommand, **kwargs) -> F:  # type: ignore
    """Command decorator function.

    Defines the command() function so that it uses the RichCommand class by default.
    """
    return __rich_global_option_wrapper(click_command, *args, cls=cls, **kwargs)


def argument(*args, cls=RichArg, **kwargs) -> F:  # type: ignore
    """Command decorator function.

    Defines the command() function so that it uses the RichCommand class by default.
    """
    return click_argument(*args, cls=cls, **kwargs)


__all__ = [
    *dir(click),
    "global_option",
    "verbose_option",
    "bg_process_option",
    "version_option",
    "group",
    "command",
    "argument",
    "RichGroup",
    "RichCommand",
    "RichConfig",
]
