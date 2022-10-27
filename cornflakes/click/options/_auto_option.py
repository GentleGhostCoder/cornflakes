from inspect import isclass
from typing import Any, Callable, TypeVar, Union

from click import Command, Group, option

from cornflakes.decorator.config import Config, ConfigGroup

F = TypeVar(
    "F",
    bound=Callable[[Union[Command, Group, Callable[..., Any]]], Union[Command, Group, Callable[..., Any], Callable]],
)


def auto_option(config: Union[Config, ConfigGroup], **options) -> F:
    """Click Option Decorator to define a global option for cli decorator."""
    if not isclass(config):
        raise TypeError("config should be a class!")

    def auto_option_decorator(callback: Union[Union[Command, Group], Callable[..., None]]):

        if not callable(callback):
            raise TypeError("Wrapped object should be a function!")

        configs = {}
        for line in config.__doc__.split("\n"):
            line = line.strip()
            if line[:5] == ":cvar":
                line = line[6:].split(":")
                configs.update({line[0]: line[1].strip()})
        for slot_name in config.__slots__:
            callback = option(f"--{slot_name.replace('_', '-')}", help=configs.get(slot_name, ""))(callback)

        return callback

    return auto_option_decorator
