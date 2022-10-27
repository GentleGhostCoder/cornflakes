from functools import wraps
from inspect import isclass
from typing import Any, Callable, Dict, List, TypeVar, Union

from click import Command, Group, option

from cornflakes.click.rich import RichCommand, RichGroup, argument
from cornflakes.decorator.config import Config, ConfigGroup, is_config

F = TypeVar(
    "F",
    bound=Callable[[Union[Command, Group, Callable[..., Any]]], Union[Command, Group, Callable[..., Any], Callable]],
)


def auto_option(config: Union[Config, ConfigGroup], **options) -> F:  # noqa: C901
    """Click Option Decorator to define a global option for cli decorator."""
    if not isclass(config):
        raise TypeError("config should be a class!")

    _is_config = is_config(config)

    def auto_option_decorator(callback: Union[Union[Command, Group, RichCommand, RichGroup], Callable[..., None]]):

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

        callback = argument("file_name", required=False, nargs=1, help="Passed Config to Method")(callback)
        if _is_config:
            callback = argument("section_name", required=False, nargs=1, help="Passed Section of Config to Method")(
                callback
            )

        @wraps(callback)
        def wrapper(*args, **kwargs):
            __config: Union[Dict[str, Union[Config, List[Config]]], ConfigGroup] = config.from_file(
                files=kwargs.get("file_name", None), sections=kwargs.get("section_name", None)
            )
            if _is_config:
                __config = __config.popitem()[1]
                if isinstance(__config, list):
                    __config = __config[1]
            kwargs.update({"config": __config})

            return callback(
                *args, **{key: value for key, value in kwargs.items() if key in callback.__code__.co_varnames}
            )

        return wrapper

    return auto_option_decorator
