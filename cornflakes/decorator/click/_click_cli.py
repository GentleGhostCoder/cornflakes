from importlib.metadata import version
from inspect import getfile
import logging
from typing import TYPE_CHECKING, Any, Callable, Optional, Type, TypeVar, Union, cast

import click
from click import style, version_option

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
from cornflakes.logging.logger import setup_logging
from cornflakes.types import Loader

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


_T = TypeVar("_T")

AnyCallable = Callable[..., Any]


def click_cli(  # noqa: C901
    callback: Optional[Any] = None,
    config: Optional[RichConfig] = None,
    files: Optional[str] = None,
    loader: Loader = Loader.DICT,
    default_log_level: int = logging.INFO,
    as_command: bool = False,
    *args,
    **kwargs,
):
    """Function that creates generic click CLI Object."""
    patch_click()
    setup_logging(default_level=default_log_level)
    if not config:
        if not files:
            config = RichConfig(*args, **kwargs)
        elif loader in [Loader.INI, Loader.YAML]:
            config = getattr(RichConfig, str(loader.name))(*args, **kwargs).popitem()[1]
        elif ".ini" in files:
            config = RichConfig.from_ini(files, *args, **kwargs).popitem()[1]
        elif ".yaml" in files:
            config = RichConfig.from_yaml(files, *args, **kwargs).popitem()[1]
        else:
            config = RichConfig(*args, **kwargs)

    def cli_wrapper(w_callback: Any):
        if not callable(w_callback):
            return w_callback

        module = getfile(w_callback)

        if hasattr(w_callback, "__module__"):
            module = w_callback.__module__.split(".", 1)[0]
            if module != "__main__":
                __version = version(module)

        module = module.replace("_", "-")

        cli: Union[Type[RichCommand], Type[RichGroup]] = (
            command(module, config=config)(w_callback) if as_command else group(module, config=config)(w_callback)
        )

        if TYPE_CHECKING:
            cli = cast(Type[RichCommand], cli) if as_command else cast(Type[RichGroup], cli)

        if cast(RichConfig, config).VERSION_INFO:
            name = w_callback.__qualname__
            __version = "0.0.1"

            version_args = {
                "prog_name": name,
                "version": __version,
                "message": style(
                    f"\033[95m{module}\033" f"[0m \033[95m" f"Version\033[0m: \033[1m" f"{__version}\033[0m"
                ),
            }
            cli = version_option(**version_args)(cli)  # type: ignore

        if cli.config.GLOBAL_OPTIONS:
            for option_obj in cli.config.GLOBAL_OPTIONS:
                cli.params.extend(option_obj.params)
        if cast(RichConfig, config).CONTEXT_SETTINGS:
            cli.context_settings = cast(RichConfig, config).CONTEXT_SETTINGS
        return cli

    return cli_wrapper(callback) if callback else cli_wrapper
