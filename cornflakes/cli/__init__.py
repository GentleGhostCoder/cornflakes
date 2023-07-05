"""Command-line interface."""
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
def cli():
    """"""


__all__ = ["cli"]

if __name__ == "__main__":
    cli()  # pragma: no cover
