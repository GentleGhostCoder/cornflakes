"""Command-line interface."""
from click import Context

from cornflakes.decorator.click import bg_process_option, group, verbose_option
from cornflakes.decorator.click.commands import command_status, command_stop
from cornflakes.decorator.click.rich import RichGroup


@group(
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
                        "--install-completion",
                    ],
                },
            ]
            for command in ["cornflakes", "cornflakes create"]
        },
    },
    COMMAND_GROUPS={},
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
    pass_context=True,
    invoke_without_command=True,
)
def cli(self: RichGroup, ctx: Context):
    """"""
    if ctx.invoked_subcommand is None:
        self.main(["--help"])


cli.add_command(command_status)
cli.add_command(command_stop)

__all__ = ["cli"]

if __name__ == "__main__":
    cli()  # pragma: no cover
