import sys

import click

from ._rich_click import rich_abort_error, rich_format_error, rich_format_help
from ._rich_command import RichCommand


class RichGroup(click.Group):
    """Richly formatted click Group.

    Inherits click.Group and overrides help and error methods
    to print richly formatted output.
    """

    command_class = RichCommand
    group_class = type

    def main(self, *args, standalone_mode: bool = True, **kwargs):
        """Main function of RichGroup."""
        try:
            rv = super().main(*args, standalone_mode=False, **kwargs)  # type: ignore
            if not standalone_mode:
                return rv
        except click.ClickException as e:
            if not standalone_mode:
                raise
            rich_format_error(e)
            sys.exit(e.exit_code)
        except click.exceptions.Abort:
            if not standalone_mode:
                raise
            rich_abort_error()
            sys.exit(1)

    def format_help(self, ctx: click.Context, formatter: click.HelpFormatter):
        """Format function of RichGroup."""
        rich_format_help(self, ctx, formatter)
