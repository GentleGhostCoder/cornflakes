from dataclasses import MISSING
import inspect
import logging
from os import environ
from typing import Any, Callable

from _cornflakes import eval_type
from cornflakes.common import check_type, extract_var_names
from cornflakes.decorator.dataclass.helper import dataclass_fields
from cornflakes.decorator.types import WITHOUT_DEFAULT

_empty = getattr(inspect, "_empty", None)


def _get_env_vars(dc_cls):
    return {key: eval_type(environ[key]) for key in dc_cls.__dataclass_fields__.keys() if key in environ.keys()}


def _validate(self, values, key, callback: Callable[..., Any]):
    try:
        co_varnames = extract_var_names(callback)
        kwargs = {}
        kwargs.update(co_varnames)
        kwargs.update({"self": self, "values": values, "key": key})
        kwargs = {key: value for key, value in kwargs.items() if key in co_varnames.keys() and value is not _empty}
        kwargs.update({key: value for key, value in values.items() if key in co_varnames.keys()})
        if len(missing := [key for key in co_varnames.keys() if key not in kwargs.keys()]) > 1:
            raise TypeError(f"Argument not provided: {missing})")
        if len(missing) == 1:
            return callback(values.pop(key), **kwargs)
        return callback(**kwargs)
    except Exception as exc:
        raise ValueError(f"Failed to validate {key} with {callback}!") from exc


def _process_validator(self, values, validators: dict, **kwargs):
    return {key: _validate(self, values, key, callback) for key, callback in validators.items() if key in kwargs}


def _process_type_checking(dc_cls, validate=False, **kwargs):
    return {
        key: check_type(getattr(dc_cls, "__annotations__", {})[key], key, value, validate=validate)
        for key, value in kwargs.items()
        if key in dataclass_fields(dc_cls).keys()
    }


def check_dataclass_kwargs(dc_cls, validate=False, **kwargs):
    """Check dataclass types."""
    kwargs.update(_process_type_checking(dc_cls, **kwargs, validate=validate))
    return kwargs


def validate_dataclass_kwargs(dc_cls, validate=False, **kwargs):
    """Validate dataclass (includes type checks + validators)."""
    _validators = {
        key: validator
        for key, value in dc_cls.__dataclass_fields__.items()
        if callable(validator := getattr(value, "validator", key))
    }

    if _validators and not validate:
        logging.warning(
            f"Validators are provided for attributes [{_validators.keys()}] in dataclass {dc_cls.__name__}, but validate is set to False!"
        )

    _required_keys = [
        key
        for key, f in dataclass_fields(dc_cls).items()
        if (f.default_factory == WITHOUT_DEFAULT) or (f.default_factory == MISSING and f.default == MISSING)
    ]

    if dc_cls.__eval_env__:
        kwargs.update(_get_env_vars(dc_cls))
    kwargs.update(_process_validator(dc_cls, kwargs, _validators, **kwargs))
    kwargs.update(_process_type_checking(dc_cls, **kwargs, validate=validate))
    if missing_keys := [key for key in _required_keys if key not in kwargs.keys()]:
        raise TypeError(f"Missing required values for keys {missing_keys} for dataclass {dc_cls.__name__}!")

    return kwargs
