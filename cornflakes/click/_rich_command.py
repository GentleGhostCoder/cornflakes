import sys
from typing import Any

import click

from cornflakes.click._rich_config import Config as RichConfig

from ._rich_click import rich_abort_error, rich_format_error, rich_format_help


class RichCommand(click.Command):
    """Richly formatted click Command.

    Inherits click.Command and overrides help and error methods
    to print richly formatted output.
    """

    standalone_mode = False

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
