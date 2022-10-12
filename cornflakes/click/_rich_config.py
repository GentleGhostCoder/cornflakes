from dataclasses import dataclass
from os import getenv
from typing import Dict, List, Literal, Optional, Union

from cornflakes._add_dataclass_slots import add_slots


@add_slots
@dataclass(frozen=True)
class Config:
    """DataClass for click config-values."""

    BASIC_OPTIONS: Optional[bool] = None  # Add Basic Options (version, verbose)

    # Default styles
    STYLE_OPTION = "bold cyan"
    STYLE_ARGUMENT = "bold cyan"
    STYLE_SWITCH = "bold green"
    STYLE_METAVAR = "bold yellow"
    STYLE_METAVAR_APPEND = "dim yellow"
    STYLE_METAVAR_SEPARATOR = "dim"
    STYLE_HEADER_TEXT = ""
    STYLE_FOOTER_TEXT = ""
    STYLE_USAGE = "yellow"
    STYLE_USAGE_COMMAND = "bold"
    STYLE_DEPRECATED = "red"
    STYLE_HELPTEXT_FIRST_LINE = ""
    STYLE_HELPTEXT = "dim"
    STYLE_OPTION_HELP = ""
    STYLE_OPTION_DEFAULT = "dim"
    STYLE_OPTION_ENVVAR = "dim yellow"
    STYLE_REQUIRED_SHORT = "red"
    STYLE_REQUIRED_LONG = "dim red"
    STYLE_OPTIONS_PANEL_BORDER = "dim"
    ALIGN_OPTIONS_PANEL = "left"
    STYLE_OPTIONS_TABLE_SHOW_LINES = False
    STYLE_OPTIONS_TABLE_LEADING = 0
    STYLE_OPTIONS_TABLE_PAD_EDGE = False
    STYLE_OPTIONS_TABLE_PADDING = (0, 1)
    STYLE_OPTIONS_TABLE_BOX = ""
    STYLE_OPTIONS_TABLE_ROW_STYLES = None
    STYLE_OPTIONS_TABLE_BORDER_STYLE = None
    STYLE_COMMANDS_PANEL_BORDER = "dim"
    ALIGN_COMMANDS_PANEL = "left"
    STYLE_COMMANDS_TABLE_SHOW_LINES = False
    STYLE_COMMANDS_TABLE_LEADING = 0
    STYLE_COMMANDS_TABLE_PAD_EDGE = False
    STYLE_COMMANDS_TABLE_PADDING = (0, 1)
    STYLE_COMMANDS_TABLE_BOX = ""
    STYLE_COMMANDS_TABLE_ROW_STYLES = None
    STYLE_COMMANDS_TABLE_BORDER_STYLE = None
    STYLE_ERRORS_PANEL_BORDER = "red"
    ALIGN_ERRORS_PANEL = "left"
    STYLE_ERRORS_SUGGESTION = "dim"
    STYLE_ABORTED = "red"
    MAX_WIDTH = int(getenv("TERMINAL_WIDTH")) if getenv("TERMINAL_WIDTH") else None  # type: ignore
    COLOR_SYSTEM: Optional[Literal["auto", "standard", "256", "truecolor", "windows"]] = "auto"
    # Set to None to disable colors
    FORCE_TERMINAL = True if getenv("GITHUB_ACTIONS") or getenv("FORCE_COLOR") or getenv("PY_COLORS") else None

    # Fixed strings
    HEADER_TEXT: Optional[str] = None
    HEADER_LOGO: Optional[str] = None
    FOOTER_TEXT: Optional[str] = None
    DEPRECATED_STRING = "(Deprecated) "
    DEFAULT_STRING = "[default: {}]"
    ENVVAR_STRING = "[env var: {}]"
    REQUIRED_SHORT_STRING = "*"
    REQUIRED_LONG_STRING = "[required]"
    RANGE_STRING = " [{}]"
    APPEND_METAVARS_HELP_STRING = "({})"
    ARGUMENTS_PANEL_TITLE = "Arguments"
    OPTIONS_PANEL_TITLE = "Options"
    COMMANDS_PANEL_TITLE: str = "Commands"
    ERRORS_PANEL_TITLE = "Error"
    ERRORS_SUGGESTION: Optional[str] = None  # Default: Try 'cmd -h' for help. Set too False to disable.
    ERRORS_EPILOGUE: Optional[str] = None
    ABORTED_TEXT = "Aborted."

    # Behaviours
    SHOW_ARGUMENTS = True  # Show positional arguments
    SHOW_METAVARS_COLUMN = True  # Show a column with the option metavar (eg. INTEGER)
    APPEND_METAVARS_HELP = False  # Append metavar (eg. [TEXT]) after the help text
    APPEND_METAVARS_REQUIRED = False  # Append metavar REQUIRED_LONG_STRING (eg. [required]) after the help text
    GROUP_ARGUMENTS_OPTIONS = False  # Show arguments with options instead of in own panel
    OPTION_ENVVAR_FIRST = False  # Show env vars before option help text instead of avert
    USE_RST = True
    USE_MARKDOWN = False  # Parse help strings as markdown
    USE_MARKDOWN_EMOJI = True  # Parse emoji codes in markdown :smile:
    USE_RICH_MARKUP = False  # Parse help strings for rich markup (eg. [red]my text[/])
    # Define sorted groups of panels to display subcommands
    USE_CLICK_SHORT_HELP = False  # Use click's default function to truncate help text

    class Groups:
        """Non DataClass for groups in click config-values."""

        COMMAND_GROUPS: Dict[str, List[Dict[str, Union[str, List[str]]]]] = {}
        # Define sorted groups of panels to display options and arguments
        OPTION_GROUPS: Dict[str, List[Dict[str, Union[str, List[str]]]]] = {}
