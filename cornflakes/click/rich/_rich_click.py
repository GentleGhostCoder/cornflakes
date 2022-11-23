import inspect
import re
import typing
from typing import Any, Generator, List, Union

import click
from rich import box
from rich.align import Align
from rich.columns import Columns
from rich.console import Console, group
from rich.emoji import Emoji
from rich.highlighter import RegexHighlighter
import rich.markdown
from rich.markdown import Markdown
from rich.padding import Padding
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.theme import Theme
from rich_rst import RestructuredText

from cornflakes.click.rich._rich_config import RichConfig as RichConfig

# Support rich <= 10.6.0
# try:
# except ImportError:
# from rich.console import render_group as group

# Rich regex highlighter
class OptionHighlighter(RegexHighlighter):
    """Highlights our special options."""

    highlights = [
        r"(^|\W)(?P<switch>\-\w+)(?![a-zA-Z0-9])",
        r"(^|\W)(?P<option>\-\-[\w\-]+)(?![a-zA-Z0-9])",
        r"(^|\W)(?P<argument>[A-Z0-9\_]+)(?![_a-zA-Z0-9])",
        r"(?P<metavar>\<[^\>]+\>)",
        r"(?P<usage>Usage: )",
    ]


highlighter = OptionHighlighter()


def get_rich_console(config: RichConfig) -> Console:
    return Console(
        theme=Theme(
            {
                "option": config.STYLE_OPTION,
                "argument": config.STYLE_ARGUMENT,
                "switch": config.STYLE_SWITCH,
                "metavar": config.STYLE_METAVAR,
                "metavar_sep": config.STYLE_METAVAR_SEPARATOR,
                "usage": config.STYLE_USAGE,
            }
        ),
        highlighter=highlighter,
        color_system=config.COLOR_SYSTEM,
        force_terminal=config.FORCE_TERMINAL,
        width=config.MAX_WIDTH,
    )


def _make_rich_rext(
    text: str, config: RichConfig, style: str = ""
) -> Union[rich.markdown.Markdown, rich.text.Text, RestructuredText]:
    """Take a string, remove indentations, and return styled text.

    By default, return the text as a Rich Text with the request style.
    If USE_RICH_MARKUP is True, also parse the text for Rich markup strings.
    If USE_MARKDOWN is True, parse as Markdown.

    Only one of USE_MARKDOWN or USE_RICH_MARKUP can be True.
    If both are True, USE_MARKDOWN takes precedence.

    Args:
        text (str): Text to style
        style (str): Rich style to apply

    Returns:
        MarkdownElement or Text: Styled text object
    """
    # Remove indentations from input text
    text = inspect.cleandoc(text)
    if config.USE_RST:
        return RestructuredText(f"| {text}")
    if config.USE_MARKDOWN:
        if config.USE_MARKDOWN_EMOJI:
            text = Emoji.replace(text)
        return Markdown(text, style=style)
    if config.USE_RICH_MARKUP:
        return highlighter(Text.from_markup(text, style=style))
    else:
        return highlighter(Text(text, style=style))


@group()
def _get_help_text(obj: Union[click.Command, click.Group], config: RichConfig) -> Generator:
    """Build primary help text for a click command or group.

    Returns the prose help text for a command or group, rendered either as a
    Rich Text object or as Markdown.
    If the command is marked as depreciated, the depreciated string will be prepended.

    Args:
        obj (click.Command or click.Group): Command or group to build help text for

    Yields:
        Text or Markdown: Multiple styled objects (depreciated, usage)
    """
    # Prepend deprecated status
    if obj.deprecated:
        yield Text(config.DEPRECATED_STRING, style=config.STYLE_DEPRECATED)

    # Fetch and dedent the help text
    help_text = inspect.cleandoc(obj.help)  # type: ignore

    # Trim off anything that comes after \f on its own line
    help_text = help_text.partition("\f")[0]

    # Get the first paragraph
    first_line = help_text.split("\n\n")[0]
    # Remove single linebreaks
    if not config.USE_MARKDOWN and not first_line.startswith("\b"):
        first_line = first_line.replace("\n", " ")
    yield _make_rich_rext(first_line.strip(), config=config, style=config.STYLE_HELPTEXT_FIRST_LINE)

    # Get remaining lines, remove single line breaks and format as dim
    remaining_paragraphs = help_text.split("\n\n")[1:]
    if len(remaining_paragraphs) > 0:
        if not config.USE_MARKDOWN:
            # Remove single linebreaks
            remaining_paragraphs = [
                x.replace("\n", " ").strip() if not x.startswith("\b") else "{}\n".format(x.strip("\b\n"))
                for x in remaining_paragraphs
            ]
            # Join back together
            remaining_lines = "\n".join(remaining_paragraphs)
        else:
            # Join with double linebreaks if markdown
            remaining_lines = "\n\n".join(remaining_paragraphs)

        yield _make_rich_rext(remaining_lines, config=config, style=config.STYLE_HELPTEXT)


# flake8: noqa: C901
def _get_parameter_help(
    param: Union[click.Option, click.Argument, click.Parameter], ctx: click.Context, config: RichConfig
) -> rich.columns.Columns:
    """Build primary help text for a click option or argument.

    Returns the prose help text for an option or argument, rendered either
    as a Rich Text object or as Markdown.
    Additional elements are appended to show the default and required status if applicable.

    Args:
        param (click.Option or click.Argument): Option or argument to build help text for
        ctx (click.Context): Click Context object

    Returns:
        Columns: A columns element with multiple styled objects (help, default, required)
    """
    items: List[Union[Markdown, Text, Any]] = []

    # Get the environment variable first
    envvar = getattr(param, "envvar", None)
    # https://github.com/pallets/click/blob/0aec1168ac591e159baf6f61026d6ae322c53aaf/src/click/core.py#L2720-L2726
    if envvar is None:
        if (
            getattr(param, "allow_from_autoenv", None)
            and getattr(ctx, "auto_envvar_prefix", None) is not None
            and param.name is not None
        ):
            envvar = f"{ctx.auto_envvar_prefix}_{param.name.upper()}"
    if envvar is not None:
        envvar = ", ".join(param.envvar) if type(envvar) is list else envvar  # type: ignore

    # Environment variable BEFORE help text
    if getattr(param, "show_envvar", None) and config.OPTION_ENVVAR_FIRST and envvar is not None:
        items.append(Text(config.ENVVAR_STRING.format(envvar), style=config.STYLE_OPTION_ENVVAR))

    # Main help text
    if getattr(param, "help", ""):
        paragraphs = param.help.split("\n\n")  # type: ignore
        # Remove single linebreaks
        if not config.USE_MARKDOWN:
            paragraphs = [
                x.replace("\n", " ").strip() if not x.startswith("\b") else "{}\n".format(x.strip("\b\n"))
                for x in paragraphs
            ]
        items.append(_make_rich_rext("\n".join(paragraphs).strip(), config=config, style=config.STYLE_OPTION_HELP))

    # Append metavar if requested
    if config.APPEND_METAVARS_HELP:
        metavar_str = param.make_metavar()
        # Do it ourselves if this is a positional argument
        if isinstance(param, click.core.Argument) and re.match(
            rf"\[?{getattr(param, 'name', '').upper()}]?", metavar_str
        ):
            metavar_str = param.type.name.upper()
        # Skip booleans
        if metavar_str != "BOOLEAN" or isinstance(param, click.core.Argument):
            metavar_str = metavar_str.replace("[", "").replace("]", "")
            items.append(
                Text(
                    config.APPEND_METAVARS_HELP_STRING.format(metavar_str),
                    style=config.STYLE_METAVAR_APPEND,
                    overflow="fold",
                )
            )

    # Environment variable AFTER help text
    if getattr(param, "show_envvar", None) and not config.OPTION_ENVVAR_FIRST and envvar is not None:
        items.append(Text(config.ENVVAR_STRING.format(envvar), style=config.STYLE_OPTION_ENVVAR))

    # Default value
    if getattr(param, "show_default", None):
        # param.default is the value, but click is a bit clever in choosing what to show here
        # eg. --debug/--no-debug, default=False will show up as [default: no-debug] instead of [default: False]
        # To avoid duplicating loads of code, let's just pull out the string from click with a regex
        # Example outputs from param.get_help_record(ctx)[-1] are:
        #     [default: foo]
        #     [env var: EMAIL, EMAIL_ADDRESS; default: foo]
        default_str_match = re.search(r"\[(?:.+; )?default: (.*)\]", typing.cast(list, param.get_help_record(ctx))[-1])
        if default_str_match:
            # Don't show the required string, as we show that afterwards anyway
            default_str = default_str_match.group(1).replace("; required", "")
            items.append(
                Text(
                    config.DEFAULT_STRING.format(default_str),
                    style=config.STYLE_OPTION_DEFAULT,
                )
            )

    # Required long?
    if config.APPEND_METAVARS_REQUIRED and param.required:
        items.append(Text(config.REQUIRED_LONG_STRING, style=config.STYLE_REQUIRED_LONG))

    # Use Columns - this allows us to group different renderable types
    # (Text, Markdown) onto a single line.
    return Columns(items)


# flake8: noqa: C901
def _make_command_help(config: RichConfig, help_text: str = "") -> Union[rich.text.Text, rich.markdown.Markdown]:
    """Build click help text for a click group command.

    That is, when calling help on groups with multiple subcommands
    (not the main help text when calling the subcommand help).

    Returns the first paragraph of help text for a command, rendered either as a
    Rich Text object or as Markdown.
    Ignores single newlines as paragraph markers, looks for double only.

    Args:
        help_text (str): Help text

    Returns:
        Text or Markdown: Styled object
    """
    paragraphs = inspect.cleandoc(help_text).split("\n\n")
    # Remove single linebreaks
    if not config.USE_MARKDOWN and not paragraphs[0].startswith("\b"):
        paragraphs[0] = paragraphs[0].replace("\n", " ")
    elif paragraphs[0].startswith("\b"):
        paragraphs[0] = paragraphs[0].replace("\b\n", "")
    return _make_rich_rext(paragraphs[0].strip(), config=config, style=config.STYLE_OPTION_HELP)


def rich_format_help(
    obj: Union[click.Command, click.Group],
    ctx: click.Context,
    formatter: click.HelpFormatter,
    config: RichConfig,
    console: Console = None,
) -> None:
    """Print nicely formatted help text using rich.

    Based on original code from rich-click, by @willmcgugan.
    https://github.com/Textualize/rich-cli/blob/8a2767c7a340715fc6fbf4930ace717b9b2fc5e5/src/rich_cli/__main__.py#L162-L236

    Replacement for the click function format_help().
    Takes a command or group and builds the help text output.

    :param formatter: Click Format Helper
    :param obj: Command or group to build help text for
    :param ctx: Click Context object
    :param config: Rich Config
    :param console: Rich Console
    """
    if not console:
        console = get_rich_console(config=config)

    # Header logo if we have it
    if config.HEADER_LOGO:
        console.print(config.HEADER_LOGO)

    # Header text if we have it
    if config.HEADER_TEXT:
        console.print(
            Padding(_make_rich_rext(config.HEADER_TEXT, config=config, style=config.STYLE_HEADER_TEXT), (1, 1, 0, 1))
        )

    # Print usage
    console.print(Padding(highlighter(obj.get_usage(ctx)), 1), style=config.STYLE_USAGE_COMMAND)

    # Print command / group help if we have some
    if obj.help:
        # Print with some padding
        console.print(
            Padding(
                Align(_get_help_text(obj, config=config), pad=False),
                (0, 1, 1, 1),
            )
        )

    # Look through OPTION_GROUPS for this command
    # stick anything unmatched into a default group at the end
    option_groups = config.OPTION_GROUPS.get(ctx.command_path, []).copy()
    option_groups.append({"options": []})
    argument_group_options = []

    for param in obj.get_params(ctx):

        # Skip positional arguments - they don't have opts or helptext and are covered in usage
        # See https://click.palletsprojects.com/en/8.0.x/documentation/#documenting-arguments
        if isinstance(param, click.core.Argument) and not config.SHOW_ARGUMENTS:
            continue

        # Skip if option is hidden
        if getattr(param, "hidden", False):
            continue

        # Already mentioned in a config option group
        for option_group in option_groups:
            if any([opt in option_group.get("options", []) for opt in param.opts]):
                break

        # No break, no mention - add to the default group
        else:
            if isinstance(param, click.core.Argument) and not config.GROUP_ARGUMENTS_OPTIONS:
                argument_group_options.append(param.opts[0])
            else:
                list_of_option_groups: List = option_groups[-1]["options"]  # type: ignore
                list_of_option_groups.append(param.opts[0])

    # If we're not grouping arguments, and we got some, prepend before default options
    if len(argument_group_options) > 0:
        extra_option_group = {"name": config.ARGUMENTS_PANEL_TITLE, "options": argument_group_options}
        option_groups.insert(len(option_groups) - 1, extra_option_group)  # type: ignore

    # Print each option group panel
    for option_group in option_groups:

        options_rows = []
        for opt in option_group.get("options", []):

            # Get the param
            for param in obj.get_params(ctx):
                if any([opt in param.opts]):
                    break
            # Skip if option is not listed in this group
            else:
                continue

            # Short and long form
            opt_long_strs = []
            opt_short_strs = []
            for idx, opt in enumerate(param.opts):
                opt_str = opt
                try:
                    opt_str += "/" + param.secondary_opts[idx]
                except IndexError:
                    pass

                if isinstance(param, click.core.Argument):
                    opt_long_strs.append(opt_str.upper())
                elif "--" in opt:
                    opt_long_strs.append(opt_str)
                else:
                    opt_short_strs.append(opt_str)

            # Column for a metavar, if we have one
            metavar = Text(style=config.STYLE_METAVAR, overflow="fold")
            metavar_str = param.make_metavar()

            # Do it ourselves if this is a positional argument
            if isinstance(param, click.core.Argument) and re.match(
                rf"\[?{getattr(param, 'name', '').upper()}]?", metavar_str
            ):
                metavar_str = param.type.name.upper()

            # Skip booleans and choices (handled above)
            if metavar_str != "BOOLEAN" or isinstance(param, click.core.Argument):
                metavar.append(metavar_str)

            # Range - from
            # https://github.com/pallets/click/blob/c63c70dabd3f86ca68678b4f00951f78f52d0270/src/click/core.py#L2698-L2706  # noqa: E501
            try:
                # skip count with default range type
                if isinstance(param.type, click.types._NumberRangeBase) and not (
                    getattr(param, "count", 0) and param.type.min == 0 and param.type.max is None
                ):
                    range_str = param.type._describe_range()
                    if range_str:
                        metavar.append(config.RANGE_STRING.format(range_str))
            except AttributeError:
                # click.types._NumberRangeBase is only in Click 8x onwards
                pass

            # Required asterisk
            required: Text = Text("")
            if param.required:
                required = Text(config.REQUIRED_SHORT_STRING, style=config.STYLE_REQUIRED_SHORT)

            # Highlighter to make [ | ] and <> dim
            class MetavarHighlighter(RegexHighlighter):
                highlights = [
                    r"^(?P<metavar_sep>(\[|<))",
                    r"(?P<metavar_sep>\|)",
                    r"(?P<metavar_sep>(\]|>)$)",
                ]

            metavar_highlighter = MetavarHighlighter()

            rows = [
                required,
                highlighter(highlighter(",".join(opt_long_strs))),
                highlighter(highlighter(",".join(opt_short_strs))),
                metavar_highlighter(metavar),
                _get_parameter_help(param, ctx, config=config),
            ]

            # Remove metavar if specified in config
            if not config.SHOW_METAVARS_COLUMN:
                rows.pop(3)

            options_rows.append(rows)

        if len(options_rows) > 0:
            t_styles = {
                "show_lines": config.STYLE_OPTIONS_TABLE_SHOW_LINES,
                "leading": config.STYLE_OPTIONS_TABLE_LEADING,
                "box": config.STYLE_OPTIONS_TABLE_BOX,
                "border_style": config.STYLE_OPTIONS_TABLE_BORDER_STYLE,
                "row_styles": config.STYLE_OPTIONS_TABLE_ROW_STYLES,
                "pad_edge": config.STYLE_OPTIONS_TABLE_PAD_EDGE,
                "padding": config.STYLE_OPTIONS_TABLE_PADDING,
            }
            t_styles.update(option_group.get("table_styles", {}))  # type: ignore
            box_style = getattr(box, t_styles.pop("box"), None)  # type: ignore
            options_table = Table(
                highlight=True,
                show_header=False,
                expand=True,
                box=box_style,
                **t_styles,  # type: ignore
            )
            # Strip the required column if none are required
            if all([x[0] == "" for x in options_rows]):
                options_rows = [x[1:] for x in options_rows]
            for row in options_rows:
                options_table.add_row(*row)  # type: ignore
            console.print(
                Panel(
                    options_table,
                    border_style=config.STYLE_OPTIONS_PANEL_BORDER,
                    title=option_group.get("name", config.OPTIONS_PANEL_TITLE),  # type: ignore
                    title_align=config.ALIGN_OPTIONS_PANEL,  # type: ignore
                )
            )

    #
    # Groups only:
    # List click command groups
    #
    if hasattr(obj, "list_commands"):
        # Look through COMMAND_GROUPS for this command
        # stick anything unmatched into a default group at the end
        cmd_groups = config.COMMAND_GROUPS.get(ctx.command_path, []).copy()
        cmd_groups.append({"commands": []})
        for command in obj.list_commands(ctx):  # type: ignore
            for cmd_group in cmd_groups:
                if command in cmd_group.get("commands", []):
                    break
            else:
                commands: List = cmd_groups[-1]["commands"]  # type: ignore
                commands.append(command)

        # Print each command group panel
        for cmd_group in cmd_groups:
            t_styles = {
                "show_lines": config.STYLE_COMMANDS_TABLE_SHOW_LINES,
                "leading": config.STYLE_COMMANDS_TABLE_LEADING,
                "box": config.STYLE_COMMANDS_TABLE_BOX,
                "border_style": config.STYLE_COMMANDS_TABLE_BORDER_STYLE,
                "row_styles": config.STYLE_COMMANDS_TABLE_ROW_STYLES,
                "pad_edge": config.STYLE_COMMANDS_TABLE_PAD_EDGE,
                "padding": config.STYLE_COMMANDS_TABLE_PADDING,
            }
            t_styles.update(cmd_group.get("table_styles", {}))  # type: ignore
            box_style = getattr(box, t_styles.pop("box"), None)  # type: ignore

            commands_table = Table(
                highlight=False,
                show_header=False,
                expand=True,
                box=box_style,
                **t_styles,  # type: ignore
            )
            # Define formatting in first column, as commands don't match highlighter regex
            commands_table.add_column(style="bold cyan", no_wrap=True)
            for command in cmd_group.get("commands", []):
                # Skip if command does not exist
                if command not in obj.list_commands(ctx):  # type: ignore
                    continue
                cmd = obj.get_command(ctx, command)  # type: ignore
                if cmd.hidden:
                    continue
                # Use the truncated short text as with vanilla text if requested
                if config.USE_CLICK_SHORT_HELP:
                    help_text = cmd.get_short_help_str()
                else:
                    # Use short_help function argument if used, or the full help
                    help_text = cmd.short_help or cmd.help or ""
                commands_table.add_row(command, _make_command_help(config=config, help_text=help_text))
            if commands_table.row_count > 0:
                console.print(
                    Panel(
                        commands_table,
                        border_style=config.STYLE_COMMANDS_PANEL_BORDER,
                        title=cmd_group.get("name", config.COMMANDS_PANEL_TITLE),  # type: ignore
                        title_align=config.ALIGN_COMMANDS_PANEL,  # type: ignore
                    )
                )

    # Epilogue if we have it
    if obj.epilog:
        # Remove single linebreaks, replace double with single
        lines = obj.epilog.split("\n\n")
        epilogue = "\n".join([x.replace("\n", " ").strip() for x in lines])
        console.print(Padding(Align(highlighter(epilogue), pad=False), 1))

    # Footer text if we have it
    if config.FOOTER_TEXT:
        console.print(
            Padding(_make_rich_rext(config.FOOTER_TEXT, config=config, style=config.STYLE_FOOTER_TEXT), (1, 1, 0, 1))
        )


def rich_format_error(self: click.ClickException, config: RichConfig, console: Console = None):
    """Print richly formatted click errors.

    Called by custom exception handler to print richly formatted click errors.
    Mimics original click.ClickException.echo() function but with rich formatting.

    Args:
        click.ClickException: Click exception to format.
    """
    if not console:
        console = get_rich_console(config=config)
    if getattr(self, "ctx", None) is not None:
        console.print(self.ctx.get_usage())  # type: ignore
    if config.ERRORS_SUGGESTION:
        console.print(config.ERRORS_SUGGESTION, style=config.STYLE_ERRORS_SUGGESTION)
    elif (
        config.ERRORS_SUGGESTION is None
        and getattr(self, "ctx", None) is not None
        and self.ctx.command.get_help_option(self.ctx) is not None  # type: ignore
    ):
        console.print(
            "Try [blue]'{command} {option}'[/] for help.".format(
                command=self.ctx.command_path, option=self.ctx.help_option_names[0]  # type: ignore
            ),
            style=config.STYLE_ERRORS_SUGGESTION,
        )

    console.print(
        Panel(
            highlighter(self.format_message()),
            border_style=config.STYLE_ERRORS_PANEL_BORDER,
            title=config.ERRORS_PANEL_TITLE,
            title_align=config.ALIGN_ERRORS_PANEL,  # type: ignore
        )
    )
    if config.ERRORS_EPILOGUE:
        console.print(config.ERRORS_EPILOGUE)


def rich_abort_error(config: RichConfig, console: Console = None) -> None:
    """Print richly formatted abort error."""
    if not console:
        console = get_rich_console(config=config)
    console.print(config.ABORTED_TEXT, style=config.STYLE_ABORTED)
