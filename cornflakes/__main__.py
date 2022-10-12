#!/usr/bin/env python
"""Command-line interface."""
from cornflakes.cli import create_new_config
from cornflakes.click import make_cli

# Banner generated with figlet and figlet-fonts/ANSI\ Shadow.flf
cornflakes_cli = make_cli(
    module="cornflakes",
    option_groups={
        "cornflakes": [
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
                ],
            },
        ],
    },
    command_groups={
        "cornflakes": [
            {
                "name": "Commands",
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
    BASIC_OPTIONS=True,
)

for command in [create_new_config]:
    cornflakes_cli.add_command(command)
    cornflakes_cli.config.Groups.COMMAND_GROUPS.get("cornflakes")[0].get("commands").append(
        command.name  # type: ignore
    )

__all__ = ["make_cli", "cornflakes_cli"]


def main():
    """Main CLI Entrypoint Method."""
    cornflakes_cli()


if __name__ == "__main__":
    main()  # pragma: no cover
