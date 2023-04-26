from importlib.metadata import version
from inspect import getfile
import logging
from typing import Any, Callable, Optional, Union

from click import BaseCommand, Command, Group, style, version_option

from cornflakes.click import RichCommand, RichConfig, RichGroup, command, group, patch_click
from cornflakes.decorator._types import Loader
from cornflakes.decorator.config import Config
from cornflakes.logging.logger import setup_logging


def click_cli(  # noqa: C901
    callback: Optional[Callable] = None,
    config: Optional[Union[Config, Any]] = None,
    files: Optional[str] = None,
    loader: Loader = Loader.DICT_LOADER,
    default_log_level: int = logging.INFO,
    as_command: bool = False,
    *args,
    **kwargs,
) -> Union[
    Callable[[Any], Callable[..., Union[BaseCommand, RichGroup]]], Callable[..., Union[BaseCommand, Group, RichGroup]]
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

    def cli_wrapper(w_callback: Callable) -> Callable[..., Union[BaseCommand, Group, RichGroup]]:
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
            cli = version_option(**version_args)(cli)

        if cli.config.GLOBAL_OPTIONS:
            for option_obj in cli.config.GLOBAL_OPTIONS:
                cli.params.extend(option_obj.params)
        if config.CONTEXT_SETTINGS:
            cli.context_settings = config.CONTEXT_SETTINGS
        return cli

    if callback:
        return cli_wrapper(callback)
    return cli_wrapper
