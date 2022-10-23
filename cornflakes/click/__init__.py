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
import logging
from typing import Callable, Union
from click import Option, option, style, version_option, Group, Command, Argument, Choice, Path  # noqa: F401, F403
from click import argument as click_argument
from click import command as click_command
from click import group as click_group

from cornflakes.click._rich_argument import RichArg
from cornflakes.click._rich_command import RichCommand
from cornflakes.click._rich_group import RichGroup
from cornflakes.click._rich_config import Config as RichConfig
from cornflakes.click.options import bg_process_option, verbose_option, global_option
from cornflakes.logging import logger


def _global_option_wrapper(click_func, *wrap_args, **wrap_kwargs) -> Callable[..., Union[Command, Group, Argument]]:
    # config = wrap_kwargs.pop("config", None)

    def global_option_click_decorator(func):

        click_cls = click_func(*wrap_args, **wrap_kwargs)(func)

        def click_callback(*func_args, **func_kwargs):
            func_kwargs["cls"] = func
            logger.setup_logging(default_level=func_kwargs.get("verbose", False) and logging.DEBUG, force=True)
            if click_cls.config and click_cls.config.GLOBAL_OPTIONS and func.__module__ != "cornflakes.click":
                for option_obj in click_cls.config.GLOBAL_OPTIONS:
                    option_obj(
                        *func_args,
                        **{key: value for key, value in func_kwargs.items() if key in option_obj.__code__.co_varnames},
                    )
            return func(
                *func_args, **{key: value for key, value in func_kwargs.items() if key in func.__code__.co_varnames}
            )

        click_cls.callback = click_callback
        return click_cls

    return global_option_click_decorator


def group(
    *args, cls=RichGroup, **kwargs
) -> Union[Union[Command, Group, Argument], Callable[..., Union[Command, Group, Argument]]]:  # type: ignore
    """Group decorator function.

    Defines the group() function so that it uses the RichGroup class by default.
    """
    return _global_option_wrapper(click_group, *args, cls=cls, **kwargs)


def command(
    *args, cls=RichCommand, **kwargs
) -> Union[Union[Command, Group, Argument], Callable[..., Union[Command, Group, Argument]]]:  # type: ignore
    """Command decorator function.

    Defines the command() function so that it uses the RichCommand class by default.
    """
    return _global_option_wrapper(click_command, *args, cls=cls, **kwargs)


def argument(
    *args, cls=RichArg, **kwargs
) -> Union[Union[Command, Group, Argument], Callable[..., Union[Command, Group, Argument]]]:  # type: ignore
    """Command decorator function.

    Defines the command() function so that it uses the RichCommand class by default.
    """
    return click_argument(*args, cls=cls, **kwargs)


__all__ = [
    "verbose_option",
    "bg_process_option",
    "version_option",
    "global_option",
    "Choice",
    "option",
    "Path",
    "group",
    "command",
    "argument",
    "style",
    "Group",
    "Command",
    "Option",
    "Argument",
    "RichGroup",
    "RichCommand",
    "RichConfig",
]
