from importlib.metadata import version
from inspect import getfile
import logging
from typing import Any, Callable, Optional, Union, cast

import click
from click import BaseCommand, Command, Group, style, version_option

from cornflakes.decorator.click.rich import (
    RichArg,
    RichCommand,
    RichConfig,
    RichGroup,
    argument,
    command,
    group,
    group_command,
    group_group,
)
from cornflakes.decorator.types import Config, Loader
from cornflakes.logging.logger import setup_logging

RICH_CLICK_PATCHED = False


def patch_click():
    """Patch click to use rich extensions."""
    global RICH_CLICK_PATCHED
    if not RICH_CLICK_PATCHED:
        click.argument = argument
        click.group = group
        click.command = command
        click.Group = RichGroup
        click.Command = RichCommand
        click.Argument = RichArg
        click.Group.command = group_command
        click.Group.group = group_group
        RICH_CLICK_PATCHED = True


def click_cli(  # noqa: C901
    callback: Optional[Callable] = None,
    config: Optional[Union[RichConfig, Config, Any]] = None,
    files: Optional[str] = None,
    loader: Loader = Loader.DICT_LOADER,
    default_log_level: int = logging.INFO,
    as_command: bool = False,
    *args,
    **kwargs,
) -> Union[
    Callable[[Any], Callable[..., Union[BaseCommand, RichGroup]]],
    Callable[..., Union[BaseCommand, Group, RichGroup, Command, RichCommand]],
]:
    """Function that creates generic click CLI Object."""
    patch_click()
    setup_logging(default_level=default_log_level)
    if not config:
        if not files:
            config = RichConfig(*args, **kwargs)
        elif loader in [Loader.INI_LOADER, Loader.YAML_LOADER]:
            config = getattr(RichConfig, str(loader.name))(*args, **kwargs).popitem()[1]
        elif ".ini" in files:
            config = RichConfig.from_ini(files, *args, **kwargs).popitem()[1]
        elif ".yaml" in files:
            config = RichConfig.from_yaml(files, *args, **kwargs).popitem()[1]
        else:
            config = RichConfig(*args, **kwargs)

    config = cast(RichConfig, config)

    def cli_wrapper(w_callback: Callable) -> Callable[..., Union[BaseCommand, Group, RichGroup, Command, RichCommand]]:
        if not callable(w_callback):
            return w_callback

        module = getfile(w_callback)
        if as_command:
            cli: Union[BaseCommand, Command, RichCommand] = command(module.split(".", 1)[0], config=config)(w_callback)
        else:
            cli: Union[BaseCommand, Group, RichGroup] = group(module.split(".", 1)[0], config=config)(w_callback)
        if config.VERSION_INFO:
            name = w_callback.__qualname__
            __version = "0.0.1"

            if hasattr(w_callback, "__module__"):
                module = w_callback.__module__.split(".", 1)[0]
                if module != "__main__":
                    __version = version(module)

            version_args = {
                "prog_name": name,
                "version": __version,
                "message": style(
                    f"\033[95m{module}\033" f"[0m \033[95m" f"Version\033[0m: \033[1m" f"{__version}\033[0m"
                ),
            }
            cli: Any = version_option(**version_args)(cli)

        if cli.config.GLOBAL_OPTIONS:
            for option_obj in cli.config.GLOBAL_OPTIONS:
                cli.params.extend(option_obj.params)
        if config.CONTEXT_SETTINGS:
            cli.context_settings = config.CONTEXT_SETTINGS
        return cli

    if callback:
        return cli_wrapper(callback)
    return cli_wrapper
