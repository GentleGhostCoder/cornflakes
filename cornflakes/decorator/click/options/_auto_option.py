from dataclasses import fields
from functools import wraps
from inspect import isclass
from typing import Any, Callable, Union

from click import Command, Group, option

from cornflakes.decorator.click.rich import RichCommand, RichGroup
from cornflakes.decorator.config import is_config
from cornflakes.decorator.dataclass.helper import dataclass_fields
from cornflakes.decorator.types import Config

F = Callable[[Union[Command, Group, Callable[..., Any]]], Union[Command, Group, Callable[..., Any], Callable]]


def auto_option(config: Union[Config, Any], config_file: bool = False, **options) -> F:  # noqa: C901
    """Click Option Decorator to define a global option for cli decorator."""
    if not isclass(config):
        raise TypeError("config should be a class!")

    _is_config = is_config(config)

    def auto_option_decorator(callback: Union[Union[Command, Group, RichCommand, RichGroup], Callable[..., None]]):
        if not callable(callback):
            raise TypeError("Wrapped object should be a function!")

        method = eval(  # noqa: S307
            f"lambda *args, {', '.join({f'{f.name}' for f in fields(config) if f.init})}, **kwargs: None"
        )

        @wraps(wraps(callback)(method))
        def wrapper(*args, **kwargs):
            config_kwargs = {key: value for key, value in kwargs.items() if key in dataclass_fields(config)}
            if "config-file" in kwargs:
                config_kwargs.update({"files": config_kwargs.pop("config-file")})

            __config = config.from_file(**config_kwargs)
            if not __config:
                raise ValueError("Config is empty!")
            if _is_config:
                __config = __config.popitem()[1]
                if isinstance(__config, list):
                    __config = __config[1]
            kwargs.update({"config": __config})

            return callback(
                *args, **{key: value for key, value in kwargs.items() if key in callback.__code__.co_varnames}
            )

        if hasattr(callback, "params"):
            wrapper.params = callback.params

        if hasattr(callback, "make_context"):
            wrapper.make_context = callback.make_context

        configs = {}
        for line in config.__doc__.split("\n"):
            line = line.strip()
            if line[:5] == ":cvar":
                line = line[6:].split(":")
                configs.update({line[0]: {"help": line[1].strip()}})

        configs.update(options)

        for slot_name in config.__dataclass_fields__.keys():
            wrapper = option(
                f"--{slot_name.replace('_', '-')}", **configs.get(slot_name, {"help": f"value for {slot_name}"})
            )(wrapper)

        if config_file:
            wrapper = option("-cfg", "--config-file", **{"help": "Config file path", "type": str})(wrapper)

        return wrapper

    return auto_option_decorator
