from functools import reduce, wraps
from inspect import isclass, signature
from os.path import exists
from typing import Any, Callable, Dict, Type, Union, cast

from click import Command, Group, option

from cornflakes.common import recursive_update
from cornflakes.decorator.click.helper import click_param_type_parser
from cornflakes.decorator.click.options._auto_fill_option_groups import auto_fill_option_groups
from cornflakes.decorator.dataclasses import (
    config_files,
    dc_slot_missing_default,
    default,
    fields,
    is_config,
    is_group,
    normalized_class_name,
)
from cornflakes.types import _T, Config, ConfigGroup, Constants, CornflakesDataclass


def _set_passed_key(wrapper, config, passing_key):
    params = signature(wrapper).parameters
    passing_keys = [param.name for param in params.values() if param.annotation == config]

    # Check if there are multiple passing_keys
    if len(passing_keys) > 1:
        raise ValueError(f"Multiple passing keys {passing_keys} are not supported. Please use a single passing key.")

    # If passing_key is not provided, get the first parameter of type from the config
    if not passing_key:
        passing_key = passing_keys[0] if passing_keys else None
        if passing_key is None:
            passing_key = normalized_class_name(config)

    # Check if the passing_key is not provided in the params
    if passing_key not in params:
        raise ValueError(
            f"Method parameter for {config.__name__} is required, when using config_option, but not provided in the parameters! You can pass the config with the key {passing_key} or by a custom parameter that has the provided config class annotation."
        )

    if passing_key in fields(config):
        raise ValueError(
            f"Key {passing_key} is part of the attributes in the config {config.__name__} use another passed_key!"
        )

    setattr(wrapper, Constants.config_option.PASSED_DECORATE_KEY, passing_key)


def _update_options_help(callback, config, formatter=None):
    if (
        "__click_params__" in dir(callback)
        and getattr(callback, "__click_params__")
        and getattr(callback, "__click_params__")[0].name == Constants.config_option.ADD_CONFIG_FILE_OPTION_PARAM_VAR
    ):
        getattr(callback, "__click_params__")[0].help = (
            formatter(getattr(callback, "__click_params__")[0].help)
            if formatter
            else f"{getattr(callback, '__click_params__')[0].help}, {config.__name__}"
        )
        return callback
    else:
        config_option_help_str = formatter("") if formatter else f"{config.__name__}"
        return option(
            Constants.config_option.ADD_CONFIG_FILE_OPTION_PARAM_SHORT,
            Constants.config_option.ADD_CONFIG_FILE_OPTION_PARAM,
            **{"help": config_option_help_str, "type": str, "multiple": True},
        )(callback)


def _config_group_option(
    config, add_config_file_options: bool = False, passing_key=None, is_sub_config=False, **options
):
    decorators: list = []  # List to hold all decorators
    sub_configs = []
    for cfg in reversed(fields(config)):  # Reverse the order of fields
        sub_config = getattr(cfg.type, "__args__", [cfg.type])[0]
        if is_config(sub_config):
            sub_configs.append(sub_config)
            decorators.append(
                _config_option(
                    config=sub_config,
                    add_config_file_options=add_config_file_options,
                    passing_key=passing_key,
                    is_sub_config=is_sub_config,
                    **options,
                )
            )

    # Function to chain decorators
    def chain_decorators(func):
        new_func = reduce(lambda f, g: g(f), decorators, func)

        def formatter(_):
            help_str = " ".join([c.__name__ for c in sub_configs])
            return f"""Add config files to init <{config.__name__}> by **DICT[{help_str}]\n\nFound default configs: {[f for f in config_files(config) if exists(f)]}"""

        if add_config_file_options:
            new_func = _update_options_help(new_func, config, formatter)

        _set_passed_key(new_func, config, passing_key)

        return new_func

    return chain_decorators  # Return the chain of decorators


AnyCallable = Callable[..., Any]


def _config_option(  # noqa: C901
    config: Union[Type[_T], Type[Config], Type[ConfigGroup]],
    add_config_file_options: bool = False,
    passing_key=None,
    is_sub_config: bool = False,
    **options,
) -> Callable[[Union[Command, Group, Type[_T], AnyCallable]], Union[Command, Group, Type[_T], AnyCallable]]:
    """Click Option Decorator to define a global option for cli decorator."""

    # parser to get click parm types for specific config
    param_parser = click_param_type_parser(config)

    # check if options are valid dict of dicts
    if not all(isinstance(v, dict) for v in options.values()):
        raise ValueError("Options should be a dict of dicts with option arguments!")

    if not is_config(config) and is_group(config):
        return _config_group_option(
            config=config,
            add_config_file_options=add_config_file_options,
            passing_key=passing_key,
            is_sub_config=True,
            **options,
        )

    def auto_option_decorator(callback):
        if not callable(callback):
            raise TypeError("Wrapped object should be a function!")

        configs: Dict[str, Dict[str, Any]] = {}
        for line in getattr(config, "__doc__", "").split("\n"):
            line = line.strip()
            if line[:5] == ":cvar":
                line = line[6:].split(":")
                configs[line[0]] = {"help": line[1].strip()}

        recursive_update(configs, options)

        wrapper = callback

        if not is_sub_config and add_config_file_options:
            wrapper = _update_options_help(wrapper, config)

        slot_options = {
            f"--{slot_name.replace('_', '-')}": slot
            for slot_name, slot in cast(Type[CornflakesDataclass], config).__dataclass_fields__.items()
        }

        for option_name, slot in slot_options.items():
            option_args = configs.get(slot.name, {})
            if "help" not in option_args:
                option_args["help"] = f"value for {slot.name}"
            if "default" not in option_args and not dc_slot_missing_default(slot):
                option_args["default"] = default(slot)
                if not slot.repr:
                    option_args["default"] = "***"
            if "type" not in option_args:
                option_args["type"] = param_parser(slot.type)()
            option_args["show_default"] = True
            wrapper = option(option_name, cls=None, **option_args)(wrapper)

        setattr(wrapper, Constants.config_option.ENABLED, True)

        def wrap_read_config(func=None):
            """Wrap the read_config function to read config from file."""

            def read_config(files=None, **kwargs):
                config_args = {k: v for k, v in kwargs.items() if k in [f.name for f in fields(config) if f.init]}
                return config.from_file(files=files, **config_args)

            return wraps(func)(read_config) if func else read_config

        # retrieve existing function
        existing_func = getattr(wrapper, Constants.config_option.READ_CONFIG_METHOD, None)
        if existing_func is None:
            # If it's the first time, we just set the new function
            setattr(wrapper, Constants.config_option.READ_CONFIG_METHOD, wrap_read_config())
        else:
            # If not the first time, wrap the existing function
            def new_func(*args, **kwargs):
                # Here you might want to define the logic for how the
                # new function interacts with the existing one.
                # For example, you might call one after the other:
                existing_result = existing_func(*args, **kwargs)
                new_result = wrap_read_config(getattr(callback, Constants.config_option.READ_CONFIG_METHOD))(
                    *args, **kwargs
                )
                recursive_update(existing_result, new_result)
                return existing_result  # or return a combination of existing_result and new_result

            setattr(wrapper, Constants.config_option.READ_CONFIG_METHOD, new_func)

        setattr(wrapper, Constants.config_option.ATTRIBUTES, {f.name for f in fields(config) if f.init})
        wrapper = auto_fill_option_groups(wrapper, config.__name__, *slot_options.keys())

        if not is_sub_config:
            _set_passed_key(wrapper, config, passing_key)

        return wrapper

    return auto_option_decorator


def config_option(  # noqa: C901
    config: Union[Type[_T], Type[CornflakesDataclass], Type[Config], Type[ConfigGroup]],
    add_config_file_options: bool = False,
    passing_key=None,
    **options,
) -> Callable[[Union[Command, Group, Type[_T], AnyCallable]], Union[Command, Group, Type[_T], AnyCallable]]:
    """Click Option Decorator to define a global option for cli decorator."""
    if not isclass(config):
        raise TypeError("config should be a class!")

    options.pop("is_sub_config", None)  # Remove is_sub_config if exists not passed by user
    return _config_option(config, add_config_file_options, passing_key, is_sub_config=False, **options)
