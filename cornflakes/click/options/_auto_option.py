from inspect import isclass
import logging
from typing import Any, Callable, Dict, List, Optional, Union

from click import Command, Group, option

from cornflakes.click.rich import RichCommand, RichGroup, argument
from cornflakes.decorator.config import Config, ConfigGroup, is_config

F = Callable[[Union[Command, Group, Callable[..., Any]]], Union[Command, Group, Callable[..., Any], Callable]]


def auto_option(config, **options) -> F:  # noqa: C901
    """Click Option Decorator to define a global option for cli decorator."""
    if not isclass(config):
        raise TypeError("config should be a class!")

    _is_config = is_config(config)

    def auto_option_decorator(callback: Union[Union[Command, Group, RichCommand, RichGroup], Callable[..., None]]):
        if not callable(callback):
            raise TypeError("Wrapped object should be a function!")

        def wrapper(config_args: Optional[tuple] = None, *args, **kwargs):
            __config: Union[Dict[str, Union[Config, List[Config]]], ConfigGroup] = config.from_file()
            if not __config:
                logging.error(f"Config is empty {__config} for file {config_args[0]} and section {config_args[1]}")
                raise ValueError
            if _is_config:
                __config = __config.popitem()[1]
                if isinstance(__config, list):
                    __config = __config[1]
            kwargs.update(
                {
                    "config": __config,
                    "config_args": config_args,
                }
            )
            return callback(
                *args, **{key: value for key, value in kwargs.items() if key in callback.__code__.co_varnames}
            )

        if hasattr(callback, "params"):
            wrapper.params = callback.params

        configs = {}
        for line in config.__doc__.split("\n"):
            line = line.strip()
            if line[:5] == ":cvar":
                line = line[6:].split(":")
                configs.update({line[0]: line[1].strip()})
        configs.update(options)
        for slot_name in config.__dataclass_fields__.keys():
            wrapper = option(
                f"--{slot_name.replace('_', '-')}", **{"help": configs.get(slot_name, f"value for {slot_name}")}
            )(wrapper)

        wrapper = argument("config_args", required=False, nargs=-1, help="Passed Config to Method")(wrapper)

        return wrapper

    return auto_option_decorator
