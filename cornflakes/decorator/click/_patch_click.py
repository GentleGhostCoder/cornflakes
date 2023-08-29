import click

from cornflakes.decorator.click.rich import (
    RichArg,
    RichCommand,
    RichGroup,
    argument,
    command,
    group,
    group_command,
    group_group,
    option,
)

RICH_CLICK_PATCHED = False


def patch_click():
    """Patch click to use rich extensions."""
    global RICH_CLICK_PATCHED
    if not RICH_CLICK_PATCHED:
        click.argument = argument
        click.group = group
        click.option = option
        click.command = command
        click.Group = RichGroup
        click.Command = RichCommand
        click.Argument = RichArg
        click.Group.command = group_command
        click.Group.group = group_group
        RICH_CLICK_PATCHED = True
