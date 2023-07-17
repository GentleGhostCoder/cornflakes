from functools import wraps
from inspect import signature
import logging
from typing import Any, Callable, Optional, Type, TypeVar

from click import get_current_context
from click.core import Context

from cornflakes.common import check_type, get_actual_type
from cornflakes.decorator.click.rich._rich_group import RichGroup
from cornflakes.decorator.dataclasses import is_config, is_group, normalized_class_name
from cornflakes.types import Constants

_T = TypeVar("_T")


def rich_global_option_wrapper(
    click_func: Any, *wrap_args, pass_context: Optional[bool] = None, **wrap_kwargs
) -> Callable[..., Type[_T]]:
    """Wrapper Method for rich command / group."""

    def global_option_click_decorator(func) -> Type[_T]:
        """Decorator for rich command / group."""
        click_cls = click_func(*wrap_args, **wrap_kwargs)(func)

        # pass __auto_options_groups__ if
        if not hasattr(click_cls, "__option_groups__"):
            click_cls.__option_groups__ = []
        click_cls.__option_groups__.extend(getattr(func, "__option_groups__", []))

        @wraps(func)
        def click_callback(*args, **kwargs):
            kwargs["self"]: RichGroup = func
            kwargs["parent"]: RichGroup = click_cls
            if pass_context:
                kwargs["ctx"]: Optional["Context"] = get_current_context()
            if click_cls.config and click_cls.config.GLOBAL_OPTIONS and func.__module__ != "cornflakes.click":
                _apply_global_options(click_cls, *args, **kwargs)

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


def _apply_auto_option_config(func, **kwargs):
    if not getattr(func, Constants.config_option.ENABLED, False):
        return kwargs

    func_params = signature(func).parameters
    passed_key = getattr(func, Constants.config_option.PASSED_DECORATE_KEY, [])
    auto_option_attributes = getattr(func, Constants.config_option.PASSED_DECORATE_KEY, [])
    config_kwargs = dict(filter(lambda kv: kv[0] in auto_option_attributes and kv[1], kwargs.items()))

    if Constants.config_option.ADD_CONFIG_FILE_OPTION_PARAM_VAR in kwargs and kwargs.get(
        Constants.config_option.ADD_CONFIG_FILE_OPTION_PARAM_VAR
    ):
        config_kwargs[Constants.config_decorator_args.FILES] = list(
            kwargs.pop(Constants.config_option.ADD_CONFIG_FILE_OPTION_PARAM_VAR, "")
        )

    kwargs[passed_key] = getattr(func, Constants.config_option.READ_CONFIG_METHOD, {})(**config_kwargs)
    config_type = get_actual_type(func_params[passed_key].annotation)
    config_name = normalized_class_name(func_params[passed_key].annotation)

    if config_name in ("list", "tuple"):
        config_name = normalized_class_name(func_params[passed_key].annotation.__args__[0])

    return _validate_and_set_config(func_params, passed_key, config_type, config_name, **kwargs)


def _validate_and_set_config(func_params, passed_key, config_type, config_name, **kwargs):
    if passed_key not in func_params:
        return

    if is_group(config_type):
        kwargs[passed_key] = check_type(config_type, passed_key, kwargs[passed_key], skip=False, validate=True)
    elif is_config(config_type):
        return _handle_config_type_validation(func_params, passed_key, config_type, config_name, **kwargs)
    elif config_type in (list, tuple):
        if config_name not in ("list", "tuple"):
            warning_msg = (
                f"For {config_name}, the is_list parameter is currently set to False, "
                "resulting in a single config where multiple configs are considered. To "
                "properly support multiple files, either change the config annotation to "
                f"<List[{func_params['config'].annotation.__args__[0].__name__}]> or modify the "
                "(...,'is_list'=True) parameter in the config decorator method."
            )
            logging.warning(warning_msg)
            kwargs[passed_key] = check_type(
                config_type,
                passed_key,
                [
                    check_type(
                        func_params["config"].annotation.__args__[0],
                        passed_key,
                        kwargs[passed_key],
                        skip=False,
                        validate=True,
                    )
                ],
                skip=False,
                validate=True,
            )
        else:
            kwargs[passed_key] = check_type(
                config_type, passed_key, kwargs[passed_key][config_name], skip=False, validate=True
            )

    return kwargs


def _handle_config_type_validation(func_params, passed_key, config_type, config_name, **kwargs):
    config_value = kwargs[passed_key][config_name]
    if isinstance(config_value, (list, tuple)):
        warning_msg = (
            f"For {config_name}, the `is_list` parameter is currently set to True, "
            "resulting in a list of configs where only the first file is considered. To "
            "properly support multiple files, either change the config annotation to "
            f"<List[{func_params['config'].annotation.__name__}]> or modify the "
            "(...,'is_list'=False) parameter in the config decorator method."
        )
        logging.warning(warning_msg)
        kwargs[passed_key] = check_type(config_type, passed_key, config_value[0], skip=False, validate=True)
    else:
        kwargs[passed_key] = check_type(config_type, passed_key, config_value, skip=False, validate=True)

    return kwargs
