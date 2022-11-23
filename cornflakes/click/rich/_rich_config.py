from dataclasses import field
from os import getenv
from typing import Dict, List, Literal, Optional, Protocol, Union

from click import Option

from cornflakes.decorator.config import config


class GlobalOption(Protocol):
    """GlobalOption Protocol which requires params."""

    params: List[Option]


@config
class RichConfig:
    """DataClass for click config-values."""

    # Default styles
    STYLE_OPTION: str = "bold cyan"
    STYLE_ARGUMENT: str = "bold cyan"
    STYLE_SWITCH: str = "bold green"
    STYLE_METAVAR: str = "bold yellow"
    STYLE_METAVAR_APPEND: str = "dim yellow"
    STYLE_METAVAR_SEPARATOR: str = "dim"
    STYLE_HEADER_TEXT: str = ""
    STYLE_FOOTER_TEXT: str = ""
    STYLE_USAGE: str = "yellow"
    STYLE_USAGE_COMMAND: str = "bold"
    STYLE_DEPRECATED: str = "red"
    STYLE_HELPTEXT_FIRST_LINE: str = ""
    STYLE_HELPTEXT: str = "dim"
    STYLE_OPTION_HELP: str = ""
    STYLE_OPTION_DEFAULT: str = "dim"
    STYLE_OPTION_ENVVAR: str = "dim yellow"
    STYLE_REQUIRED_SHORT: str = "red"
    STYLE_REQUIRED_LONG: str = "dim red"
    STYLE_OPTIONS_PANEL_BORDER: str = "dim"
    ALIGN_OPTIONS_PANEL: str = "left"
    STYLE_OPTIONS_TABLE_SHOW_LINES = False
    STYLE_OPTIONS_TABLE_LEADING = 0
    STYLE_OPTIONS_TABLE_PAD_EDGE = False
    STYLE_OPTIONS_TABLE_PADDING = (0, 1)
    STYLE_OPTIONS_TABLE_BOX: str = ""
    STYLE_OPTIONS_TABLE_ROW_STYLES = None
    STYLE_OPTIONS_TABLE_BORDER_STYLE = None
    STYLE_COMMANDS_PANEL_BORDER: str = "dim"
    ALIGN_COMMANDS_PANEL: str = "left"
    STYLE_COMMANDS_TABLE_SHOW_LINES = False
    STYLE_COMMANDS_TABLE_LEADING = 0
    STYLE_COMMANDS_TABLE_PAD_EDGE = False
    STYLE_COMMANDS_TABLE_PADDING = (0, 1)
    STYLE_COMMANDS_TABLE_BOX: str = ""
    STYLE_COMMANDS_TABLE_ROW_STYLES = None
    STYLE_COMMANDS_TABLE_BORDER_STYLE = None
    STYLE_ERRORS_PANEL_BORDER: str = "red"
    ALIGN_ERRORS_PANEL: str = "left"
    STYLE_ERRORS_SUGGESTION: str = "dim"
    STYLE_ABORTED: str = "red"
    MAX_WIDTH = int(getenv("TERMINAL_WIDTH")) if getenv("TERMINAL_WIDTH") else None  # type: ignore
    COLOR_SYSTEM: Optional[Literal["auto", "standard", "256", "truecolor", "windows"]] = "auto"
    # Set to None to disable colors
    FORCE_TERMINAL = True if getenv("GITHUB_ACTIONS") or getenv("FORCE_COLOR") or getenv("PY_COLORS") else None

    # Fixed strings
    HEADER_TEXT: Optional[str] = None
    HEADER_LOGO: Optional[str] = None
    FOOTER_TEXT: Optional[str] = None
    DEPRECATED_STRING: str = "(Deprecated) "
    DEFAULT_STRING: str = "[default: {}]"
    ENVVAR_STRING: str = "[env var: {}]"
    REQUIRED_SHORT_STRING: str = "*"
    REQUIRED_LONG_STRING: str = "[required]"
    RANGE_STRING: str = " [{}]"
    APPEND_METAVARS_HELP_STRING: str = "({})"
    ARGUMENTS_PANEL_TITLE: str = "Arguments"
    OPTIONS_PANEL_TITLE: str = "Options"
    COMMANDS_PANEL_TITLE: str = "Commands"
    ERRORS_PANEL_TITLE: str = "Error"
    ERRORS_SUGGESTION: Optional[str] = None  # Default: Try 'cmd -h' for help. Set too False to disable.
    ERRORS_EPILOGUE: Optional[str] = None
    ABORTED_TEXT: str = "Aborted."

    # Behaviours
    SHOW_ARGUMENTS: bool = True  # Show positional arguments
    SHOW_METAVARS_COLUMN: bool = True  # Show a column with the option metavar (eg. INTEGER)
    APPEND_METAVARS_HELP: bool = False  # Append metavar (eg. [TEXT]) after the help text
    APPEND_METAVARS_REQUIRED: bool = False  # Append metavar REQUIRED_LONG_STRING (eg. [required]) after the help text
    GROUP_ARGUMENTS_OPTIONS: bool = False  # Show arguments with options instead of in own panel
    OPTION_ENVVAR_FIRST: bool = False  # Show env vars before option help text instead of avert
    USE_RST: bool = True
    USE_MARKDOWN: bool = False  # Parse help strings as markdown
    USE_MARKDOWN_EMOJI: bool = True  # Parse emoji codes in markdown :smile:
    USE_RICH_MARKUP: bool = False  # Parse help strings for rich markup (eg. [red]my text[/])
    # Define sorted groups of panels to display subcommands
    USE_CLICK_SHORT_HELP: bool = False  # Use click's default function to truncate help text

    VERSION_INFO: bool = False

    CONTEXT_SETTINGS: Dict[str, List[Dict[str, Union[str, List[str]]]]] = field(default_factory=dict)

    COMMAND_GROUPS: Dict[str, List[Dict[str, Union[str, List[str]]]]] = field(default_factory=dict)
    # Define sorted groups of panels to display options and arguments
    OPTION_GROUPS: Dict[str, List[Dict[str, Union[str, List[str]]]]] = field(default_factory=dict)
    # Add basic global options (verbose)
    GLOBAL_OPTIONS: List[GlobalOption] = field(default_factory=list)
