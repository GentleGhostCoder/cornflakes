from importlib.metadata import version
from inspect import getfile
import logging
from typing import TYPE_CHECKING, Any, Callable, Optional, TypeVar, Union, cast

from click import Command, Group, MultiCommand, style, version_option

from cornflakes.decorator._wrap_kwargs import wrap_kwargs
from cornflakes.decorator.click._patch_click import patch_click
from cornflakes.decorator.click.options import bg_process_option, verbose_option
from cornflakes.decorator.click.rich import RichCommand, RichConfig, RichGroup, command, group
from cornflakes.decorator.dataclasses import dataclass_fields
from cornflakes.logging.logger import setup_logging
from cornflakes.types import Loader

_T = TypeVar("_T")

AnyCallable = Callable[..., Any]


@wrap_kwargs(RichConfig)
def click_cli(  # noqa: C901
    *args,
    callback: Optional[Any] = None,
    config: Optional[RichConfig] = None,
    files: Optional[str] = None,
    loader: Loader = Loader.DICT,
    default_log_level: int = logging.INFO,
    as_command: bool = False,
    **kwargs,
):
    """Function that creates generic click CLI Object."""
    patch_click()
    setup_logging(default_level=default_log_level)
    if not config:
        config_args = {key: value for key, value in kwargs.items() if key in dataclass_fields(RichConfig)}
        if not files:
            config = RichConfig(**config_args)
        elif loader in [Loader.INI, Loader.YAML]:
            config = getattr(RichConfig, str(loader.name))(**config_args).popitem()[1]
        elif ".ini" in files:
            config = RichConfig.from_ini(files, **config_args).popitem()[1]
        elif ".yaml" in files:
            config = RichConfig.from_yaml(files, **config_args).popitem()[1]
        else:
            config = RichConfig(**config_args)

    def cli_wrapper(w_callback: Any):
        if not callable(w_callback):
            return w_callback

        module = getfile(w_callback)

        if hasattr(w_callback, "__module__"):
            module = w_callback.__module__.split(".", 1)[0]
            if module != "__main__":
                __version = version(module)

        module = module.replace("_", "-")

        if ("name" not in kwargs or not kwargs["name"]) and not (args and isinstance(args[0], str)):
            kwargs["name"] = module

        cli: Union[RichCommand, RichGroup] = (
            command(
                *args,
                config=config,
                **{
                    key: value
                    for key, value in kwargs.items()
                    if key in [*RichCommand.__init__.__code__.co_varnames, *Command.__init__.__code__.co_varnames]
                },
            )(w_callback)
            if as_command
            else group(
                *args,
                config=config,
                **{
                    key: value
                    for key, value in kwargs.items()
                    if key
                    in [
                        *RichGroup.__init__.__code__.co_varnames,
                        *Group.__init__.__code__.co_varnames,
                        *MultiCommand.__init__.__code__.co_varnames,
                    ]
                },
            )(w_callback)
        )

        if TYPE_CHECKING:
            cli = cast(RichCommand, cli) if as_command else cast(RichGroup, cli)

        if cast(RichConfig, config).VERSION_INFO:
            name = w_callback.__qualname__
            __version = version(module)

            version_args = {
                "prog_name": name,
                "version": __version,
                "message": style(
                    f"\033[95m{module}\033" f"[0m \033[95m" f"Version\033[0m: \033[1m" f"{__version}\033[0m"
                ),
            }
            cli = version_option(**version_args)(cli)  # type: ignore

        if cast(RichConfig, config).VERBOSE_OPTION and verbose_option not in cli.config.GLOBAL_OPTIONS:
            cli.config.GLOBAL_OPTIONS.append(verbose_option)

        if cast(RichConfig, config).BG_PROCESS_OPTION and bg_process_option not in cli.config.GLOBAL_OPTIONS:
            cli.config.GLOBAL_OPTIONS.append(bg_process_option)

        if cli.config.GLOBAL_OPTIONS:
            for option_obj in cli.config.GLOBAL_OPTIONS:
                cli.params.extend(option_obj.params)
        if cast(RichConfig, config).CONTEXT_SETTINGS:
            cli.context_settings = cast(RichConfig, config).CONTEXT_SETTINGS
        return cli

    return cli_wrapper(callback) if callback else cli_wrapper
