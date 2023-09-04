from functools import wraps
from inspect import signature
import logging
from typing import Any, Callable, Optional

from click import get_current_context
from click.core import Context

from cornflakes.common import check_type, get_actual_type, recursive_update
from cornflakes.decorator.dataclasses import is_config, is_group, normalized_class_name
from cornflakes.types import Constants


def rich_global_option_wrapper(click_func: Callable[..., Any], *wrap_args, **wraped_kwargs):
    """Wrapper Method for rich command / group."""

    def global_option_click_decorator(func):
        """Decorator for rich command / group."""
        click_cls = click_func(*wrap_args, **wraped_kwargs)(func)

        # pass __auto_options_groups__ if
        if not hasattr(click_cls, Constants.config_option.OPTION_GROUPS):
            setattr(click_cls, Constants.config_option.OPTION_GROUPS, [])

        getattr(click_cls, Constants.config_option.OPTION_GROUPS).extend(
            getattr(func, Constants.config_option.OPTION_GROUPS, [])
        )

        @wraps(func)
        def click_callback(*args, **kwargs):
            kwargs["self"] = click_cls
            if getattr(click_cls, "pass_context", False):
                kwargs["ctx"]: Optional["Context"] = get_current_context()
            if click_cls.config and click_cls.config.GLOBAL_OPTIONS and func.__module__ != "cornflakes.click":
                _apply_global_options(click_cls, *args, **kwargs)
                _apply_option_groups(click_cls)

            kwargs = _apply_auto_option_config(func, **kwargs)
            return func(
                *args, **{key: value for key, value in kwargs.items() if key in signature(func).parameters.keys()}
            )

        click_cls.callback = click_callback

        return click_cls

    return global_option_click_decorator


def _apply_global_options(click_cls, *args, **kwargs):
    for option_obj in click_cls.config.GLOBAL_OPTIONS:
        option_obj(*args, **dict(filter(lambda kv: kv[0] in signature(option_obj).parameters.keys(), kwargs.items())))


def _apply_option_groups(click_cls):
    if hasattr(click_cls, Constants.config_option.OPTION_GROUPS) and hasattr(click_cls, "config"):
        for option_group_obj in getattr(click_cls, Constants.config_option.OPTION_GROUPS, []):
            recursive_update(click_cls.config.OPTION_GROUPS, option_group_obj, merge_lists=True)


def _apply_auto_option_config(func, **kwargs):
    if not getattr(func, Constants.config_option.ENABLED, False):
        return kwargs

    func_params = signature(func).parameters
    auto_option_attributes = getattr(func, Constants.config_option.ATTRIBUTES, [])
    config_kwargs = dict(filter(lambda kv: kv[0] in auto_option_attributes and kv[1], kwargs.items()))

    if Constants.config_option.ADD_CONFIG_FILE_OPTION_PARAM_VAR in kwargs and kwargs.get(
        Constants.config_option.ADD_CONFIG_FILE_OPTION_PARAM_VAR
    ):
        config_kwargs[Constants.config_decorator_args.FILES] = list(
            kwargs.pop(Constants.config_option.ADD_CONFIG_FILE_OPTION_PARAM_VAR, "")
        )

    read_configs = getattr(func, Constants.config_option.READ_CONFIG_METHOD)(**config_kwargs)
    recursive_update(kwargs, read_configs, merge_lists=True)
    passed_keys = getattr(func, Constants.config_option.PASSED_DECORATE_KEYS, None)
    for passed_key in passed_keys or []:
        if passed_key not in func_params:
            continue
        config_type = get_actual_type(func_params[passed_key].annotation)
        config_name = normalized_class_name(func_params[passed_key].annotation)
        if config_name in ("list", "tuple"):
            config_name = normalized_class_name(func_params[passed_key].annotation.__args__[0])

        kwargs = _validate_and_set_config(func_params, passed_key, config_type, config_name, **kwargs)
    return kwargs


def _validate_and_set_config(func_params, passed_key, config_type, config_name, **kwargs):
    if passed_key not in func_params:
        return

    if is_group(config_type):
        kwargs[passed_key] = check_type(config_type, kwargs[passed_key], passed_key, skip=False)
    elif is_config(config_type):
        return _handle_config_type_validation(func_params, passed_key, config_type, config_name, **kwargs)
    elif config_type in (list, tuple):
        if config_name not in ("list", "tuple"):
            # warning_msg = (
            #     f"For {config_name}, the is_list parameter is currently set to False, "
            #     "resulting in a single config where multiple configs are considered. To "
            #     "properly support multiple files, either change the config annotation to "
            #     f"<List[{func_params[passed_key].annotation.__args__[0].__name__}]> or modify the "
            #     "(...,'is_list'=True) parameter in the config decorator method."
            # )
            # logging.warning(warning_msg)
            kwargs[passed_key] = check_type(
                func_params[passed_key].annotation, kwargs[passed_key], passed_key, skip=False
            )
        else:
            kwargs[passed_key] = check_type(config_type, kwargs[passed_key][config_name], passed_key, skip=False)

    return kwargs


def _handle_config_type_validation(func_params, passed_key, config_type, config_name, **kwargs):
    sections = getattr(config_type, Constants.config_decorator.SECTIONS, [])
    sections.extend([name for name in [config_name, passed_key] if name not in sections])

    # config_value -> first found section in kwargs that exists. otherwise raise error

    config_value = next(
        (kwargs[section] for section in sections if section in kwargs and kwargs[section] is not None), None
    )

    if config_value is None:
        raise ValueError(f"Could not find any config value with keys {sections} in kwargs {kwargs}")

    if isinstance(config_value, (list, tuple)):
        warning_msg = (
            f"For {config_name}, the `is_list` parameter is currently set to True, "
            "resulting in a list of configs where only the first file is considered. To "
            "properly support multiple files, either change the config annotation to "
            f"<List[{func_params[passed_key].annotation.__name__}]> or modify the "
            "(...,'is_list'=False) parameter in the config decorator method."
        )
        logging.warning(warning_msg)
        kwargs[passed_key] = check_type(config_type, config_value[0], passed_key, skip=False)
    else:
        kwargs[passed_key] = check_type(config_type, config_value, passed_key, skip=False)

    return kwargs
