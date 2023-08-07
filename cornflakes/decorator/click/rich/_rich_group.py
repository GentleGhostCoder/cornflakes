import sys
from typing import Any, Dict, List, Optional, Union

from click import ClickException, Command, Context, Group, HelpFormatter, Parameter, exceptions

from cornflakes.common import recursive_update
from cornflakes.decorator.click.helper import get_command_name
from cornflakes.decorator.click.rich._rich_click import (
    get_rich_console,
    rich_abort_error,
    rich_format_error,
    rich_format_help,
)
from cornflakes.decorator.click.rich._rich_command import RichCommand
from cornflakes.decorator.click.rich._rich_config import RichConfig as RichConfig
from cornflakes.types import Constants


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
    config: RichConfig
    pass_context: Optional[bool] = False

    def callback(self):
        """Callback method with is wrapped over the command group."""

    def add_command(self, cmd: Union[Command, RichCommand, Group, Any], name: Optional[str] = None) -> None:
        """Registers another :class:`Command` with this group.

        If the name is not provided, the name of the command is used.
        """
        setattr(cmd, "parent", self)
        # pass __auto_options_groups__ if
        Group.add_command(self, cmd, name)

    def __init__(self, *args, pass_context: Optional[bool] = None, config: Optional[RichConfig] = None, **kwargs):
        """Init function of RichGroup with extra config argument."""
        if not config:
            config = RichConfig()
        super().__init__(*args, **kwargs)
        self.config = config
        self.pass_context = pass_context
        self.console = get_rich_console(config=self.config)

    def __pass_config(self, config=None, console=None):
        if not config:
            return
        for _group in self.commands.values():
            _group.parent = self
            if isinstance(_group, RichGroup) and _group:
                _group.__pass_config(config, console)
            _group.config = config
            _group.console = console or get_rich_console(_group.config)
            if _group.config.GLOBAL_OPTIONS:
                for option_obj in _group.config.GLOBAL_OPTIONS:
                    _group.params.extend(option_obj.params)

            # fill the auto-options if exists
            command = get_command_name(_group)
            if hasattr(_group, Constants.config_option.OPTION_GROUPS) and len(
                getattr(_group, Constants.config_option.OPTION_GROUPS, {})
            ):
                update_dict = {command: getattr(_group, Constants.config_option.OPTION_GROUPS, {})}
                recursive_update(_group.config.OPTION_GROUPS, update_dict, merge_lists=True)

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
