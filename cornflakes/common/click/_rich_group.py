import sys
from typing import Any

import click

from cornflakes.common.click._rich_config import Config as RichConfig
from cornflakes.common.click._rich_config import default_config

from ._rich_click import rich_abort_error, rich_format_error, rich_format_help
from ._rich_command import RichCommand


class RichGroup(click.Group):
    """Richly formatted click Group.

    Inherits click.Group and overrides help and error methods
    to print richly formatted output.
    """

    command_class = RichCommand
    group_class = type

    def __init__(self, config: RichConfig = None, *args, **kwargs):
        """Init function of RichGroup with extra config argument."""
        self.config = config or default_config
        super().__init__(*args, **kwargs)

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
