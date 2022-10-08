"""Main CLI module for cornflakes."""
import cornflakes
from cornflakes.common import click
from typing import no_type_check as typeguard_ignore

from ._create import create_new_config

# Banner generated with figlet and figlet-fonts/ANSI\ Shadow.flf
click.Config.HEADER_LOGO = """[blue]
 ██████╗ ██████╗ ██████╗ ███╗   ██╗███████╗██╗      █████╗ ██╗  ██╗███████╗ ███████╗
██╔════╝██╔═══██╗██╔══██╗████╗  ██║██╔════╝██║     ██╔══██╗██║ ██╔╝██╔════╝ ██╔════╝
██║     ██║   ██║██████╔╝██╔██╗ ██║█████╗  ██║     ███████║█████╔╝ █████╗   ███████╗
██║     ██║   ██║██╔══██╗██║╚██╗██║██╔══╝  ██║     ██╔══██║██╔═██╗ ██╔══╝   ╚════██║
╚██████╗╚██████╔╝██║  ██║██║ ╚████║██║     ███████╗██║  ██║██║  ██╗███████╗ ███████║
 ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚══════╝"""

# click.Config.HEADER_TEXT = (
#    "The [IONOS ML CLI](https://gitlab.df.server.lan/sgeist/cornflakes) "
#    "is used in order to communicate with the ML Services TSS.\n"
# )

click.Config.Groups.OPTION_GROUPS = {
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
}
click.Config.Groups.COMMAND_GROUPS = {
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
}

click.Config.Groups.CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}  # for more see. click/core.py


@typeguard_ignore
@click.group
@click.version_option(
    prog_name="cornflakes",
    version=cornflakes.__version__,
    message=click.style(f"\033[95mcornflakes\033[0m \033[95mVersion\033[0m: \033[1m{cornflakes.__version__}\033[0m"),
)
def cli():
    """Create generic any easy to manage Configs for your Project."""  # noqa: D400, D401
    pass


for command in [create_new_config]:
    cli.add_command(command)
    click.Config.Groups.COMMAND_GROUPS.get("cornflakes")[0].get("commands").append(command.name)  # type: ignore

for command in []:
    cli.add_command(command)
    click.Config.Groups.COMMAND_GROUPS.get("cornflakes")[1].get("commands").append(command.name)  # type: ignore

__all__ = ["cli"]
