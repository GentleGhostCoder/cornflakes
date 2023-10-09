from functools import wraps
from inspect import Parameter, signature
from typing import Any, Callable, Optional

from click import Command, Group, get_current_context
from click.core import Context

from cornflakes.common import recursive_update
from cornflakes.decorator.click.rich._rich_command import RichCommand
from cornflakes.decorator.click.rich._rich_group import RichGroup
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
        sig = signature(option_obj)
        params = kwargs

        if isinstance(option_obj, (Command, RichCommand, Group, RichGroup)):
            raise ValueError("Global options should not be a click.Command or click.Group instance.")

        # pass arguments to key-arguments
        param_names = list(sig.parameters.keys())
        params.update(dict(zip(param_names, args)))

        if not any(p.kind == Parameter.VAR_KEYWORD for p in sig.parameters.values()):
            params = dict(filter(lambda kv: kv[0] in sig.parameters.keys(), params.items()))

        option_obj(**params)


def _apply_option_groups(click_cls):
    if hasattr(click_cls, Constants.config_option.OPTION_GROUPS) and hasattr(click_cls, "config"):
        for option_group_obj in getattr(click_cls, Constants.config_option.OPTION_GROUPS, []):
            recursive_update(click_cls.config.OPTION_GROUPS, option_group_obj, merge_lists=True)


def _apply_auto_option_config(func, **kwargs):
    if not getattr(func, Constants.config_option.ENABLED, False):
        return kwargs

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
