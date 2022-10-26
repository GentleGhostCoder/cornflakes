import sys
from typing import Any

import click

from cornflakes.click._rich_config import Config as RichConfig

from ._rich_click import get_rich_console, rich_abort_error, rich_format_error, rich_format_help
from ._rich_command import RichCommand


class RichGroup(click.Group):
    """Richly formatted click Group.

    Inherits click.Group and overrides help and error methods
    to print richly formatted output.
    """

    command_class = RichCommand
    group_class = type
    params = []
    name = ""
    context_settings = {}
    commands = []

    def callback(self):
        """Callback method with is wrapped over the command group."""
        pass

    def __init__(self, config: RichConfig = None, *args, **kwargs):
        """Init function of RichGroup with extra config argument."""
        super().__init__(*args, **kwargs)
        self.config = config or None
        self.console = None

    def __pass_config(self, config=None, console=None):
        if config:
            for group in self.commands.values():
                if isinstance(group, RichGroup) and group:
                    group.__pass_config(config, console)
                group.config = config
                group.console = console if console else get_rich_console(group.config)
                if group.config.GLOBAL_OPTIONS:
                    for option_obj in group.config.GLOBAL_OPTIONS:
                        group.params.extend(option_obj.params)

    def main(self, *args, standalone_mode: bool = True, **kwargs) -> Any:  # noqa: C901
        """Main function of RichGroup."""
        try:
            self.console = get_rich_console(config=self.config)
            self.__pass_config(self.config, self.console)
            rv = super().main(*args, standalone_mode=False, **kwargs)  # type: ignore
            if not standalone_mode:
                return rv
        except click.ClickException as e:
            if not standalone_mode:
                raise
            rich_format_error(e, config=self.config, console=self.console)
            sys.exit(e.exit_code)
        except click.exceptions.Abort:
            if not standalone_mode:
                raise
            rich_abort_error(config=self.config, console=self.console)
            sys.exit(1)

    def format_help(self, ctx: click.Context, formatter: click.HelpFormatter) -> None:
        """Format function of RichGroup."""
        rich_format_help(self, ctx, formatter, config=self.config, console=self.console)
