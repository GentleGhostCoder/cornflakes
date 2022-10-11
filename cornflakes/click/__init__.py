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

import click
import pkg_resources
from click import *  # noqa: F401, F403
from click import argument as click_argument
from click import command as click_command
from click import group as click_group

from cornflakes.click._rich_argument import RichArg
from cornflakes.click._rich_command import RichCommand
from cornflakes.click._rich_group import RichGroup
from cornflakes.click._rich_config import Config as RichConfig
from cornflakes.logger import DefaultLogger


def group(*args, cls=RichGroup, **kwargs) -> click_group:  # type: ignore
    """Group decorator function.

    Defines the group() function so that it uses the RichGroup class by default.
    """
    return click_group(*args, cls=cls, **kwargs)


def command(*args, cls=RichCommand, **kwargs) -> click_command:  # type: ignore
    """Command decorator function.

    Defines the command() function so that it uses the RichCommand class by default.
    """
    return click_command(*args, cls=cls, **kwargs)


def argument(*args, cls=RichArg, **kwargs) -> click_argument:  # type: ignore
    """Command decorator function.

    Defines the command() function so that it uses the RichCommand class by default.
    """
    return click_argument(*args, cls=cls, **kwargs)


click.Group = RichGroup  # type: ignore
click.Command = RichCommand  # type: ignore

if TYPE_CHECKING:
    from click import Choice, Path, option, version_option, style  # noqa: F401


def make_cli(
    module: str,
    option_groups: dict = None,
    command_groups: dict = None,
    context_settings: dict = None,
    set_logger: bool = False,
    *args,
    **kwargs,
):
    """Function that creates generic click CLI Object."""
    config = RichConfig(*args, **kwargs)

    if option_groups:
        config.Groups.OPTION_GROUPS = option_groups
    if command_groups:
        config.Groups.COMMAND_GROUPS = command_groups

    if set_logger:

        @group(module)
        @option("--log-level", default=logging.INFO, help="Log-Level for the global logger.", required=False)
        @option("--log-config", default="logging.yaml", help="Log-config file path for logger.", required=False)
        @option(
            "--verbose",
            "-v",
            default=False,
            type=bool,
            is_flag=True,
            show_default=True,
            help="Flag to set logger to debug mode.",
            required=False,
        )
        @version_option(
            prog_name=module,
            version=pkg_resources.get_distribution(module).version,
            message=click.style(
                f"\033[95m{module}\033"
                f"[0m \033[95mVersion\033[0m: \033[1m"
                f"{pkg_resources.get_distribution(module).version}\033[0m"
            ),
        )
        def cli(log_level: int, log_config: str, verbose: bool):
            if verbose:
                log_level = logging.DEBUG
            DefaultLogger.setup_logging(default_level=log_level, default_path=log_config)

    else:

        @group(module)
        @version_option(
            prog_name=module,
            version=pkg_resources.get_distribution(module).version,
            message=click.style(
                f"\033[95m{module}\033"
                f"[0m \033[95mVersion\033[0m: \033[1m"
                f"{pkg_resources.get_distribution(module).version}\033[0m"
            ),
        )
        def cli():
            pass

    cli.config = config

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
