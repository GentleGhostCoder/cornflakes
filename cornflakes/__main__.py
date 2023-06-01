"""Command-line interface."""
import logging

import click

from cornflakes.decorator import click_cli
from cornflakes.decorator.click import bg_process_option, verbose_option


@click_cli(
    OPTION_GROUPS={
        **{
            command: [
                {
                    "name": "Basic Options",
                    "options": [
                        "--name",
                        "--description",
                        "--help",
                        "--log-level",
                        "--log-config",
                        "--version",
                        "--verbose",
                        "--silent",
                        "--background-process",
                    ],
                },
            ]
            for command in ["cornflakes", "cornflakes create"]
        },
    },
    COMMAND_GROUPS={
        "cornflakes": [
            {
                "name": "Test Commands",
                "commands": ["print"],
            },
        ]
    },
    CONTEXT_SETTINGS={"help_option_names": ["-h", "--help"]},
    HEADER_LOGO="""[blue]
 ██████╗ ██████╗ ██████╗ ███╗   ██╗███████╗██╗      █████╗ ██╗  ██╗███████╗ ███████╗
██╔════╝██╔═══██╗██╔══██╗████╗  ██║██╔════╝██║     ██╔══██╗██║ ██╔╝██╔════╝ ██╔════╝
██║     ██║   ██║██████╔╝██╔██╗ ██║█████╗  ██║     ███████║█████╔╝ █████╗   ███████╗
██║     ██║   ██║██╔══██╗██║╚██╗██║██╔══╝  ██║     ██╔══██║██╔═██╗ ██╔══╝   ╚════██║
╚██████╗╚██████╔╝██║  ██║██║ ╚████║██║     ███████╗██║  ██║██║  ██╗███████╗ ███████║
 ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚══════╝""",
    # Banner generated with figlet and figlet-fonts/ANSI\ Shadow.flf
    HEADER_TEXT="Create generic any easy to manage Configs for your Project.",
    GLOBAL_OPTIONS=[verbose_option, bg_process_option],
    VERSION_INFO=True,
)
def main():
    """Main CLI Entrypoint Method."""


@main.group("print")
def print_group():
    """Test Group."""


logger = logging.getLogger("new_logger")


@print_group.command("hello")
def hello_world_command(verbose):
    """Hello World Command."""
    click.echo("Hello World!")
    logger.info("Info log message test.")
    logger.debug("Debug log message test.")


__all__ = ["main"]

if __name__ == "__main__":
    main()  # pragma: no cover
