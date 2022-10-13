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
"""  # noqa: RST303 D205
import logging
from typing import TYPE_CHECKING

import pkg_resources
from click import option, style, version_option, pass_obj  # noqa: F401, F403
from click import argument as click_argument
from click import command as click_command
from click import group as click_group

from cornflakes.click._rich_argument import RichArg
from cornflakes.click._rich_command import RichCommand
from cornflakes.click._rich_group import RichGroup, verbose_option
from cornflakes.click._rich_config import Config as RichConfig
from cornflakes.logging import logger

if TYPE_CHECKING:
    from click import Choice, Path  # noqa: F401


def _verbose_wrapper(click_func, *wrap_args, **wrap_kwargs):
    def wrapper_command(func):
        def wrapper_func(verbose=False, *func_args, **func_kwargs):
            if verbose:
                logger.setup_logging(default_level=logging.DEBUG)
            return func(*func_args, **func_kwargs)

        return click_func(*wrap_args, **wrap_kwargs)(wrapper_func)

    return wrapper_command


def group(*args, cls=RichGroup, **kwargs) -> click_group:  # type: ignore
    """Group decorator function.

    Defines the group() function so that it uses the RichGroup class by default.
    """
    return _verbose_wrapper(click_group, *args, cls=cls, **kwargs)


def command(*args, cls=RichCommand, **kwargs) -> click_command:  # type: ignore
    """Command decorator function.

    Defines the command() function so that it uses the RichCommand class by default.
    """
    return _verbose_wrapper(click_command, *args, cls=cls, **kwargs)


def argument(*args, cls=RichArg, **kwargs) -> click_argument:  # type: ignore
    """Command decorator function.

    Defines the command() function so that it uses the RichCommand class by default.
    """
    return click_argument(*args, cls=cls, **kwargs)


def make_cli(
    module: str,
    option_groups: dict = None,
    command_groups: dict = None,
    context_settings: dict = None,
    *args,
    **kwargs,
):
    """Function that creates generic click CLI Object."""
    config = RichConfig(*args, **kwargs)

    if option_groups:
        config.Groups.OPTION_GROUPS = option_groups
    if command_groups:
        config.Groups.COMMAND_GROUPS = command_groups

    @group(module)
    @version_option(
        prog_name=module,
        version=pkg_resources.get_distribution(module).version,
        message=style(
            f"\033[95m{module}\033"
            f"[0m \033[95mVersion\033[0m: \033[1m"
            f"{pkg_resources.get_distribution(module).version}\033[0m"
        ),
    )
    def cli():
        pass

    cli.config = config
    if cli.config.BASIC_OPTIONS:
        cli.params.append(verbose_option)
    if context_settings:
        cli.context_settings = context_settings

    return cli


__all__ = [
    "make_cli",
    "argument",
    "Choice",
    "option",
    "Path",
    "version_option",
    "group",
    "command",
    "RichGroup",
    "RichCommand",
    "RichConfig",
]
