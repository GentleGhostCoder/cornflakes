import sys
from typing import Any, List, Optional

from click import ClickException, Command, Context, HelpFormatter, Parameter, exceptions

from cornflakes.decorator.click.rich._rich_click import rich_abort_error, rich_format_error, rich_format_help
from cornflakes.decorator.click.rich._rich_config import RichConfig as RichConfig


class RichCommand(Command):
    """Richly formatted click Command.

    Inherits click.Command and overrides help and error methods
    to print richly formatted output.
    """

    standalone_mode = False
    params: List[Parameter]
    allow_extra_args = True
    allow_interspersed_args = False
    ignore_unknown_options = False
    name = ""
    context_settings: dict
    parent = None
    config: RichConfig

    def callback(self):
        """Callback method with is wrapped over the command."""

    def __init__(self, *args, config: Optional[RichConfig] = None, **kwargs):
        """Init function of RichGroup with extra config argument."""
        if not config:
            config = RichConfig()
        super().__init__(*args, **kwargs)
        self.config = config
        self.console = None

    def main(self, *args, standalone_mode: bool = True, **kwargs) -> Any:  # noqa: C901
        """Main function of RichGroup."""
        try:
            rv = super().main(*args, standalone_mode=False, **kwargs)  # type: ignore
            if not standalone_mode:
                return rv
        except ClickException as e:
            if not standalone_mode:
                raise
            rich_format_error(e, config=self.config)
            sys.exit(e.exit_code)
        except exceptions.Abort:
            if not standalone_mode:
                raise
            rich_abort_error(config=self.config)
            sys.exit(1)

    def format_help(self, ctx: Context, formatter: HelpFormatter) -> None:
        """Format function of RichGroup."""
        rich_format_help(self, ctx, formatter, config=self.config)
