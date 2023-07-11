from functools import wraps
from inspect import signature
from typing import Any, Callable, Optional, Union

from click import get_current_context
from click.core import Context

from _cornflakes import eval_type
from cornflakes.decorator.click.rich._rich_argument import RichArg
from cornflakes.decorator.click.rich._rich_command import RichCommand
from cornflakes.decorator.click.rich._rich_group import RichGroup

F = Callable[..., Union[RichCommand, RichGroup, RichArg, Any]]


def rich_global_option_wrapper(click_func, *wrap_args, pass_context: Optional[bool] = None, **wrap_kwargs) -> F:
    """Wrapper Method for rich command / group."""

    def global_option_click_decorator(func):
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
            if click_cls.config and (click_cls.config.GLOBAL_OPTIONS and func.__module__ != "cornflakes.click"):
                for option_obj in click_cls.config.GLOBAL_OPTIONS:
                    option_obj(
                        *args,
                        **{
                            key: value
                            for key, value in kwargs.items()
                            if key in signature(option_obj).parameters.keys()
                        },
                    )
            if getattr(func, "__auto_option_enabled__", False):
                config_kwargs = {
                    key: value
                    for key, value in kwargs.items()
                    if key in getattr(func, "__auto_option_attributes__", []) and value
                }
                if "config_file" in kwargs and kwargs.get("config_file"):
                    config_kwargs["files"] = eval_type(kwargs.pop("config_file", ""))
                kwargs["config"]: Any = getattr(func, "__auto_option_init__", lambda **k: k)(**config_kwargs)
            return func(
                *args, **{key: value for key, value in kwargs.items() if key in signature(func).parameters.keys()}
            )

        click_cls.callback = click_callback

        return click_cls

    return global_option_click_decorator
