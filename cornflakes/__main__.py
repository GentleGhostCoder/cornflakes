#!/usr/bin/env python
"""Command-line interface."""
from cornflakes.cli import create_new_config
from cornflakes.click import RichGroup, bg_process_option, verbose_option
from cornflakes.decorator import click_cli


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
                "name": "Commands",
                "commands": [],
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
    GLOBAL_OPTIONS=[verbose_option, bg_process_option, verbose_option],
)
def main():
    """Main CLI Entrypoint Method."""
    pass


if isinstance(main, RichGroup):
    for command in [create_new_config]:
        main.add_command(command)
        main.config.COMMAND_GROUPS.get("cornflakes")[0].get("commands").append(command.name)  # type: ignore

__all__ = ["main"]

if __name__ == "__main__":
    main()  # pragma: no cover
