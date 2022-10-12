import sys
from typing import Any, Optional, Union

import click

from cornflakes.click._rich_config import Config as RichConfig

from ._rich_click import rich_abort_error, rich_format_error, rich_format_help
from ._rich_command import RichCommand

verbose_option = click.Option(
    ["-v", "--verbose"],
    count=True,
    default=0,
    help="Base logging level is set to logging.DEBUG.",
)


class RichGroup(click.Group):
    """Richly formatted click Group.

    Inherits click.Group and overrides help and error methods
    to print richly formatted output.
    """

    command_class = RichCommand
    group_class = type

    def add_command(self, cmd: Union[RichCommand, Any], name: Optional[str] = None) -> None:
        """Wrapper of click.core.Groud.add_command to pass configs.

        Registers another :class:`Command` with this group.  If the name
        is not provided, the name of the command is used.
        """
        if not cmd.config:
            cmd.config = self.config
        if cmd.config.BASIC_OPTIONS:
            cmd.params.append(verbose_option)
        click.core.Group.add_command(self, cmd, name)

        # click.core.Group.add_command(self, cmd_wrapper, name)

    def __init__(self, config: RichConfig = None, *args, **kwargs):
        """Init function of RichGroup with extra config argument."""
        super().__init__(*args, **kwargs)
        self.config = config or None

    def main(self, *args, standalone_mode: bool = True, **kwargs) -> Any:
        """Main function of RichGroup."""
        try:
            rv = super().main(*args, standalone_mode=False, **kwargs)  # type: ignore
            if not standalone_mode:
                return rv
        except click.ClickException as e:
            if not standalone_mode:
                raise
            rich_format_error(e, config=self.config)
            sys.exit(e.exit_code)
        except click.exceptions.Abort:
            if not standalone_mode:
                raise
            rich_abort_error(config=self.config)
            sys.exit(1)

    def format_help(self, ctx: click.Context, formatter: click.HelpFormatter) -> None:
        """Format function of RichGroup."""
        rich_format_help(self, ctx, formatter, config=self.config)
