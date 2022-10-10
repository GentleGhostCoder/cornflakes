"""Main CLI module for cornflakes."""
import pkg_resources

from cornflakes.common import click
from typing import no_type_check as typeguard_ignore
from cornflakes.common.click import RichConfig

from ._create import create_new_config


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


# Banner generated with figlet and figlet-fonts/ANSI\ Shadow.flf
cornflakes_cli = make_cli(
    module="cornflakes",
    option_groups={
        "cornflakes": [
            {
                "name": "Basic options",
                "options": ["--name", "--description", "--version", "--help"],
            },
        ],
        "cornflakes get": [
            {
                "name": "Basic options",
                "options": ["--name", "--description", "--help"],
            },
        ],
    },
    command_groups={
        "cornflakes": [
            {
                "name": "API commands",
                "commands": [],
            },
            {
                "name": "Setup commands",
                "commands": [],
            },
        ]
    },
    context_settings={"help_option_names": ["-h", "--help"]},
    HEADER_LOGO="""[blue]
  ██████╗ ██████╗ ██████╗ ███╗   ██╗███████╗██╗      █████╗ ██╗  ██╗███████╗ ███████╗
 ██╔════╝██╔═══██╗██╔══██╗████╗  ██║██╔════╝██║     ██╔══██╗██║ ██╔╝██╔════╝ ██╔════╝
 ██║     ██║   ██║██████╔╝██╔██╗ ██║█████╗  ██║     ███████║█████╔╝ █████╗   ███████╗
 ██║     ██║   ██║██╔══██╗██║╚██╗██║██╔══╝  ██║     ██╔══██║██╔═██╗ ██╔══╝   ╚════██║
 ╚██████╗╚██████╔╝██║  ██║██║ ╚████║██║     ███████╗██║  ██║██║  ██╗███████╗ ███████║
  ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚══════╝""",
    HEADER_TEXT=("Create generic any easy to manage Configs for your Project."),
)

for command in [create_new_config]:
    cornflakes_cli.add_command(command)
    cornflakes_cli.config.Groups.COMMAND_GROUPS.get("cornflakes")[0].get("commands").append(
        command.name  # type: ignore
    )

for command in []:
    cornflakes_cli.add_command(command)
    cornflakes_cli.config.Groups.COMMAND_GROUPS.get("cornflakes")[1].get("commands").append(
        command.name  # type: ignore
    )

__all__ = ["make_cli", "cornflakes_cli"]
