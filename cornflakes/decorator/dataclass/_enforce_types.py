from contextlib import suppress
import inspect
from itertools import chain
from os import environ
from typing import Any, Callable, Optional, Union, get_args

from _cornflakes import eval_type
from cornflakes.common import extract_var_names, wrap_kwargs
from cornflakes.decorator._types import WITHOUT_DEFAULT, Config, ConfigGroup, DataclassProtocol

SpecialForm = type(Optional)

_empty = getattr(inspect, "_empty", None)


def enforce_types(config: Union[DataclassProtocol, Config, ConfigGroup], validate=False):  # noqa: C901
    """Adds a simple decorator enforce_types that enables enforcing strict typing on a function or dataclass using annotations.

    Works with collection types and subtypes for example Dict[str, Tuple[int, int]], and with special types as Optional and Any.
    Base Reference: https://github.com/matchawine/python-enforce-typing
    """
    validators = {
        key: validator
        for key, value in config.__dataclass_fields__.items()
        if callable(validator := getattr(value, "validator", key))
    }

    required_keys = [
        key
        for key, value in config.__dataclass_fields__.items()
        if getattr(value, "default_factory", None) == WITHOUT_DEFAULT
    ]

    def _check_type(type_hint: Any, key, value, skip=False):
        if isinstance(type_hint, type(None)):
            return

        if isinstance(type_hint, SpecialForm):
            return value

        with suppress(KeyError):

            actual_type: Any = getattr(type_hint, "__origin__", getattr(type_hint, "type", type_hint))

            if isinstance(actual_type, SpecialForm):
                actual_type = getattr(type_hint, "__args__", type_hint)

            if isinstance(actual_type, list) or isinstance(actual_type, tuple):
                actual_types = [t for t in actual_type if t is not None]
                if not any(inspect.isclass(t) for t in actual_types):
                    if value not in actual_types:
                        raise TypeError(
                            f"Expected any of '{actual_types}' for attribute '{key}' but received type '{type(value)}')."
                        )
                    actual_types = [type(t) for t in actual_types]
                values = [_check_type(t, key, value, skip=True) for t in actual_types]
                if not any(values) and type(None) in actual_types:
                    return None
                return next(item for item in values if item is not None)

            if actual_type in [list, tuple]:
                if not isinstance(value, list) and not isinstance(value, tuple):
                    if skip:
                        return
                    raise TypeError(
                        f"Expected type '{type_hint}' for attribute '{key}' but received type '{type(value)}')."
                    )
                actual_types = [t for t in get_args(type_hint) if t is not None] or [str]
                return actual_type(chain([_check_type(t, key, val) for val in value for t in actual_types]))

            if not inspect.isclass(actual_type):
                actual_type = type(actual_type)

            if not isinstance(value, actual_type):
                try:
                    if not validate:
                        if skip:
                            return
                        raise TypeError(
                            f"Expected type '{type_hint}' for attribute '{key}' but received type '{type(value)}')."
                        )
                    return actual_type(value)  # type: ignore
                except Exception as exc:
                    if skip:
                        return
                    raise Exception(
                        f"\n{exc}"
                        f"Expected type '{type_hint}' for attribute '{key}' but received type '{type(value)}')."
                    ) from exc

            return value

    def _get_env_vars():
        return {key: eval_type(environ[key]) for key in config.__dataclass_fields__.keys() if key in environ.keys()}

    def _validate(self, values, key, callback: Callable[..., Any]):
        try:
            co_varnames = extract_var_names(callback)
            kwargs = {}
            kwargs.update(co_varnames)
            kwargs.update({"self": self, "values": values, "key": key})
            kwargs.update(values)
            kwargs = {key: value for key, value in kwargs.items() if key in co_varnames.keys() and value is not _empty}
            if len(missing := [key for key in co_varnames.keys() if key not in kwargs.keys()]) > 1:
                raise TypeError(f"Argument not provided: {missing})")
            if len(missing) == 1:
                return callback(values.pop(key), **kwargs)
            return callback(**kwargs)
        except Exception as exc:
            raise Exception(f"Failed to validate {key} with {callback}!") from exc

    def _process_validator(self, values, validators: dict, **kwargs):
        return {
            key: _validate(self, values, key, callback) for key, callback in validators.items() if key in kwargs.keys()
        }

    def _process_type_checking(**kwargs):
        return {
            key: _check_type(getattr(config, "__annotations__", {})[key], key, value)
            for key, value in kwargs.items()
            if key in config.__dataclass_fields__.keys()
        }

    def decorate(func):
        @wrap_kwargs(func)
        def wrapper(self, *args, **kwargs):
            kwargs.update(dict(zip(func.__code__.co_varnames[1:], args)))
            default_kwargs = {}
            default_kwargs.update(kwargs)

            if self.__eval_env__:
                default_kwargs.update(_get_env_vars())

            default_kwargs.update(_process_validator(self, default_kwargs, validators, **default_kwargs))

            default_kwargs.update(_process_type_checking(**default_kwargs))
            default_kwargs.pop("self", None)
            if missing_keys := [key for key in required_keys if key not in default_kwargs.keys()]:
                raise ValueError(f"Missing required values for keys {missing_keys}")

            return func(self, **default_kwargs)  # type: ignore

        return wrapper

    config.__init__ = decorate(config.__init__)

    return config
