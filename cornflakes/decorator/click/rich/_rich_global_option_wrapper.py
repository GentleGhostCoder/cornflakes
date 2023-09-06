from functools import wraps
from inspect import signature
from typing import Any, Callable, Optional

from click import get_current_context
from click.core import Context

from cornflakes.common import recursive_update
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

    signature(func).parameters
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
    return kwargs
