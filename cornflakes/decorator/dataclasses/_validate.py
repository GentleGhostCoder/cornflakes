from copy import copy
from inspect import signature
import logging
from types import SimpleNamespace
from typing import Any, Callable, Dict, List

from cornflakes.common import check_type, extract_var_names, has_return_statement
from cornflakes.decorator.dataclasses._helper import (
    dataclass_fields,
    dataclass_init_exclude_keys,
    dataclass_required_keys,
    dataclass_validators,
    default,
    get_env_vars,
    is_eval_env,
)
from cornflakes.types import INSPECT_EMPTY_TYPE, WITHOUT_DEFAULT_TYPE

logger = logging.getLogger(__name__)


def _check_validator_return_type(callback, dc_types, key):
    if return_type := signature(callback).return_annotation:
        if return_type == INSPECT_EMPTY_TYPE:
            if not has_return_statement(callback):
                return False
            raise TypeError(
                f"Validator callback {callback} for {key} "
                f"requires a type hint of {dc_types.get(key)} for the return statements!"
            )
        if dc_types.get(key) != return_type:
            raise TypeError(
                f"Validator callback {callback} has the return type {return_type}, "
                f"which is not match the type hint {dc_types.get(key)}!"
            )
        return True


def _check_all_validator_return_type(validators, dc_types):
    return [_check_validator_return_type(callback, dc_types, key) for key, callback in validators.items()]


def _handle_validate_return(value, values, key, callback, has_return, values_ns):
    values.update(vars(values_ns))
    if has_return:
        return value
    if key not in values:
        raise TypeError(f"Callback {callback} has no return statement and does not provide a value for {key}!")
    return values.get(key)


def _validate(cls, values, key, callback: Callable[..., Any], has_return):
    try:
        co_varnames = extract_var_names(callback)
        kwargs = {}
        kwargs.update(co_varnames)
        values_ns = type(
            f"SimpleNamespace<{cls.__name__}>",
            (SimpleNamespace,),
            {
                k: v
                for k, v in cls.__dict__.items()
                if callable(v) and k not in values and k not in ["__init__", "__setattr__"]
            },
        )(**values)
        kwargs.update({"cls": cls, "self": values_ns})
        kwargs = {
            key: value for key, value in kwargs.items() if key in co_varnames.keys() and value is not INSPECT_EMPTY_TYPE
        }
        kwargs.update({key: value for key, value in values.items() if key in co_varnames.keys()})
        if len(missing := [key for key in co_varnames.keys() if key not in kwargs.keys()]) > 1:
            raise TypeError(f"Some Arguments not provided by init dataclass values: {missing})")
        if len(missing) == 1:
            # in some cases co_var names does not contain the wrapped argument (e.g. `func`)
            return _handle_validate_return(
                callback(values.pop(key), **kwargs), values, key, callback, has_return, values_ns
            )
        return _handle_validate_return(callback(**kwargs), values, key, callback, has_return, values_ns)
    except TypeError as e:
        raise TypeError(f"Error while validating {key} for {cls.__name__}: {e}")


def _process_validator(self, values, validators: dict, validators_has_returns, **kwargs):
    return {
        key: _validate(self, values, key, callback, has_return)
        for (key, callback), has_return in zip(validators.items(), validators_has_returns)
        if key in kwargs
    }


def _process_type_checking(dc_cls, dc_types, **kwargs):
    return {
        key: check_type(dc_types.get(key), kwargs.get(key), key)
        for key in kwargs.keys()
        if key in dataclass_fields(dc_cls).keys()
    }


def get_dataclass_non_comparable_kwargs(field_defaults: dict) -> List[Any]:
    """Check if all fields are naturally comparable using ==.
    Returns a list of field names that are not comparable.
    """
    non_comparable_fields = []

    for field_name, default_value in field_defaults.items():
        try:
            # Try to create a copy of the default value
            copied_value = copy(default_value)

            # Try to compare the copied value with the original
            if copied_value != default_value:
                non_comparable_fields.append(field_name)
        except Exception:
            non_comparable_fields.append(field_name)

    return non_comparable_fields


def check_dataclass_kwargs(dc_cls, **kwargs) -> Dict[str, Any]:
    """Check dataclass types."""
    _fields = dataclass_fields(dc_cls)
    _dc_types = {key: _fields.get(key).type for key in kwargs.keys()}
    kwargs.update(_process_type_checking(dc_cls, _dc_types, **kwargs))
    return kwargs


def validate_dataclass_kwargs(dc_cls, force=True, **kwargs):
    """Validate dataclass (includes type checks + validators)."""

    _fields = dataclass_fields(dc_cls)

    _validators = dataclass_validators(dc_cls)
    _required_keys = dataclass_required_keys(dc_cls)
    _init_exclude_keys = dataclass_init_exclude_keys(dc_cls)

    # extend init values with the default values for init fields
    kwargs.update(
        {field.name: default(field) for field in _fields.values() if field.name not in [*kwargs, *_init_exclude_keys]}
    )

    _dc_types = {key: _fields.get(key).type for key in kwargs.keys() if key in _fields}

    if not force:
        # remove required_keys that have kwargs WITHOUT_DEFAULT_TYPE that has without default
        kwargs = {
            key: value
            for key, value in kwargs.items()
            if not (key in _required_keys and isinstance(value, WITHOUT_DEFAULT_TYPE))
        }

    if is_eval_env(dc_cls):
        kwargs.update(get_env_vars(dc_cls))

    _validators_has_returns = _check_all_validator_return_type(_validators, _dc_types)

    if _validators and force:
        # run all validators if force is True
        kwargs.update(_process_validator(dc_cls, kwargs, _validators, _validators_has_returns, **kwargs))
    kwargs.update(_process_type_checking(dc_cls, _dc_types, **kwargs))

    # # remove _init_exclude_keys from kwargs if they are added
    kwargs = {key: value for key, value in kwargs.items() if key not in _init_exclude_keys}

    if not force:
        # skip missing keys check if force is False
        return kwargs

    if missing_keys := [key for key in _required_keys if key not in kwargs.keys()]:
        raise TypeError(f"Missing required values for keys {missing_keys} for dataclass {dc_cls.__name__}!")

    return kwargs
