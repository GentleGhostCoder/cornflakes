from dataclasses import fields
from functools import reduce, wraps
from inspect import isclass
from typing import Any, Callable, Optional, Union

from click import Command, Group, option

from cornflakes.decorator.click.helper import click_param_type_parser
from cornflakes.decorator.click.options._auto_fill_option_groups import auto_fill_option_groups
from cornflakes.decorator.click.rich import RichCommand, RichGroup
from cornflakes.decorator.config import is_config
from cornflakes.decorator.dataclass.helper import dc_slot_get_default, dc_slot_missing_default, is_group
from cornflakes.decorator.types import Config

F = Callable[[Union[Command, Group, Callable[..., Any]]], Union[Command, Group, Callable[..., Any], Callable]]
SpecialForm = type(Optional)


def auto_option(config: Union[Config, Any], config_file: bool = False, **options) -> F:  # noqa: C901
    """Click Option Decorator to define a global option for cli decorator."""
    if not isclass(config):
        raise TypeError("config should be a class!")

    if not is_config(config) and is_group(config):
        decorators = []  # List to hold all decorators
        for cfg in reversed(fields(config)):  # Reverse the order of fields
            sub_config = getattr(cfg.type, "__args__", [cfg.type])[0]
            if is_config(sub_config):
                decorators.append(auto_option(sub_config, config_file=config_file, **options))

        # Function to chain decorators
        def chain_decorators(func):
            return reduce(lambda f, g: g(f), decorators, func)

        return chain_decorators  # Return the chain of decorators

    # parser to get click parm types for specific config
    param_parser = click_param_type_parser(config)

    def auto_option_decorator(callback: Union[Union[Command, Group, RichCommand, RichGroup], Callable[..., None]]):
        if not callable(callback):
            raise TypeError("Wrapped object should be a function!")

        configs = {}
        for line in config.__doc__.split("\n"):
            line = line.strip()
            if line[:5] == ":cvar":
                line = line[6:].split(":")
                configs[line[0]] = {"help": line[1].strip()}

        configs.update(options)

        wrapper = callback

        slot_options = {
            f"--{slot_name.replace('_', '-')}": slot for slot_name, slot in config.__dataclass_fields__.items()
        }

        for option_name, slot in slot_options.items():
            option_args = configs.get(slot.name, {})
            if "help" not in option_args:
                option_args["help"] = f"value for {slot.name}"
            if "default" not in option_args:
                if dc_slot_missing_default(slot):
                    option_args["required"] = "True"
                else:
                    option_args["default"] = dc_slot_get_default(slot)
            if "type" not in option_args:
                option_args["type"] = param_parser(slot.type)()
            wrapper = option(option_name, **option_args)(wrapper)

        if config_file:
            wrapper = option(
                "-cfg", "--config-file", **{"help": "Config file path", "type": param_parser(Union[str, list])()}
            )(wrapper)

        wrapper.__auto_option_enabled__ = True

        def wrap_init(func):
            @wraps(func)
            def wrapper_init(files=None, **kwargs):
                init_config = {}
                if hasattr(func, "__auto_option_init__"):
                    init_config = func.__auto_option_init__(**kwargs)
                config_args = {
                    key: value for key, value in kwargs.items() if key in [f.name for f in fields(config) if f.init]
                }
                raw_config = config.from_file(files=files, skip_missing=True, **config_args)
                init_config.update(raw_config)
                return init_config

            return wrapper_init

        setattr(wrapper, "__auto_option_init__", wrap_init(callback.__init__))
        setattr(wrapper, "__auto_option_attributes__", {f.name for f in fields(config) if f.init})
        wrapper = auto_fill_option_groups(wrapper, config.__name__, *slot_options.keys())
        return wrapper

    return auto_option_decorator
