from functools import wraps
from inspect import isclass
from typing import Any, Callable, Dict, List, TypeVar, Union

from cornflakes.click import Command, Group, argument, option
from cornflakes.decorator.config import Config, ConfigGroup, is_config

F = TypeVar(
    "F",
    bound=Callable[[Union[Command, Group, Callable[..., Any]]], Union[Command, Group, Callable[..., Any], Callable]],
)


def auto_option(config: Union[Config, ConfigGroup], **options) -> F:  # noqa: C901
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
        configs.update(options)
        for slot_name in config.__slots__:
            callback = option(f"--{slot_name.replace('_', '-')}", help=configs.get(slot_name, ""))(callback)

        callback = argument("file_name", type=str, required=False, nargs=1, help="Passed Config to Method")(callback)
        if is_config(config):
            callback = argument(
                "section_name", type=str, required=False, nargs=1, help="Passed Section of Config to Method"
            )(callback)

        @wraps(callback)
        def wrapper(file_name: str = None, section_name: str = None, **kwargs):
            __config: Union[Dict[str, Union[Config, List[Config]]], ConfigGroup] = config.from_file(
                files=file_name, sections=section_name, **kwargs
            )
            if file_name and section_name:
                __config = __config.popitem()[1]
                if isinstance(__config, list):
                    __config = __config[1]
            return callback(config=__config)

        return wrapper

    return auto_option_decorator
