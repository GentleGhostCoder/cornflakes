import sys
from typing import Any, Dict, List, Optional, Union

from click import ClickException, Command, Context, Group, HelpFormatter, Parameter, exceptions

from cornflakes.click.rich._rich_click import get_rich_console, rich_abort_error, rich_format_error, rich_format_help
from cornflakes.click.rich._rich_command import RichCommand
from cornflakes.click.rich._rich_config import RichConfig as RichConfig


class RichGroup(Group):
    """Richly formatted click Group.

    Inherits click.Group and overrides help and error methods
    to print richly formatted output.
    """

    command_class = RichCommand
    group_class = type
    params: List[Parameter]
    name = ""
    context_settings: dict
    commands: Dict[str, Union[Command, RichCommand]]

    def callback(self):
        """Callback method with is wrapped over the command group."""
        pass

    def add_command(self, cmd: Union[Command, RichCommand], name: Optional[str] = None) -> None:
        """Registers another :class:`Command` with this group.

        If the name is not provided, the name of the command is used.
        """
        Group.add_command(self, cmd, name)

    def __init__(self, config: RichConfig = None, *args, **kwargs):
        """Init function of RichGroup with extra config argument."""
        if not config:
            config = RichConfig()
        super().__init__(*args, **kwargs)
        self.config = config
        self.console = get_rich_console(config=self.config)

    def __pass_config(self, config=None, console=None):
        if config:
            for _group in self.commands.values():
                if isinstance(_group, RichGroup) and _group:
                    _group.__pass_config(config, console)
                _group.config = config
                _group.console = console if console else get_rich_console(_group.config)
                if _group.config.GLOBAL_OPTIONS:
                    for option_obj in _group.config.GLOBAL_OPTIONS:
                        _group.params.extend(option_obj.params)

    def main(self, *args, standalone_mode: bool = True, **kwargs) -> Any:  # noqa: C901
        """Main function of RichGroup."""
        try:
            self.__pass_config(self.config, self.console)
            rv = super().main(*args, standalone_mode=False, **kwargs)  # type: ignore
            if not standalone_mode:
                return rv
        except ClickException as e:
            if not standalone_mode:
                raise
            rich_format_error(e, config=self.config, console=self.console)
            sys.exit(e.exit_code)
        except exceptions.Abort:
            if not standalone_mode:
                raise
            rich_abort_error(config=self.config, console=self.console)
            sys.exit(1)

    def format_help(self, ctx: Context, formatter: HelpFormatter) -> None:
        """Format function of RichGroup."""
        rich_format_help(self, ctx, formatter, config=self.config, console=self.console)
