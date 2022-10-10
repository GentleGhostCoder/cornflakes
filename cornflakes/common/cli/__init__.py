"""Main CLI module for cornflakes."""
import pkg_resources

from cornflakes.common import click
from typing import no_type_check as typeguard_ignore
from cornflakes.common.click import RichConfig


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
    if context_settings:
        config.Groups.CONTEXT_SETTINGS = context_settings

    @typeguard_ignore
    @click.group
    @click.version_option(
        prog_name=module,
        version=pkg_resources.get_distribution(module).version,
        message=click.style(
            f"\033[95m{module}\033"
            f"[0m \033[95mVersion\033[0m: \033[1m"
            f"{pkg_resources.get_distribution(module).version}\033[0m"
        ),
    )
    def cli():  # noqa: D103
        pass

    cli.config = config

    return cli
