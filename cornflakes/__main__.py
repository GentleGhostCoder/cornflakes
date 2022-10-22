#!/usr/bin/env python
"""Command-line interface."""
from cornflakes.cli import create_new_config
from cornflakes.click import bg_process_option, make_cli, verbose_option

# Banner generated with figlet and figlet-fonts/ANSI\ Shadow.flf
cornflakes_cli = make_cli(
    __name__,
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
                "name": "Commands",
                "commands": [],
            },
        ]
    },
    CONTEXT_SETTINGS={"help_option_names": ["-h", "--help"]},
    HEADER_LOGO="""[blue]
 #  ██████╗ ██████╗ ██████╗ ███╗   ██╗███████╗██╗      █████╗ ██╗  ██╗███████╗ ███████╗
 # ██╔════╝██╔═══██╗██╔══██╗████╗  ██║██╔════╝██║     ██╔══██╗██║ ██╔╝██╔════╝ ██╔════╝
 # ██║     ██║   ██║██████╔╝██╔██╗ ██║█████╗  ██║     ███████║█████╔╝ █████╗   ███████╗
 # ██║     ██║   ██║██╔══██╗██║╚██╗██║██╔══╝  ██║     ██╔══██║██╔═██╗ ██╔══╝   ╚════██║
 # ╚██████╗╚██████╔╝██║  ██║██║ ╚████║██║     ███████╗██║  ██║██║  ██╗███████╗ ███████║
 #  ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚══════╝""",
    HEADER_TEXT="Create generic any easy to manage Configs for your Project.",
    GLOBAL_OPTIONS=[verbose_option, bg_process_option],
)

for command in [create_new_config]:
    cornflakes_cli.add_command(command)
    cornflakes_cli.config.COMMAND_GROUPS.get("cornflakes")[0].get("commands").append(command.name)  # type: ignore

__all__ = ["make_cli", "cornflakes_cli"]


def main():
    """Main CLI Entrypoint Method."""
    cornflakes_cli()


if __name__ == "__main__":
    main()  # pragma: no cover
