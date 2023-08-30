import logging
from types import SimpleNamespace
from typing import Any, Callable, Dict

from cornflakes.common import check_type, extract_var_names, has_return_statement
from cornflakes.decorator.dataclasses._helper import (
    dataclass_fields,
    dataclass_required_keys,
    dataclass_validators,
    default,
    get_env_vars,
    is_eval_env,
)
from cornflakes.types import INSPECT_EMPTY_TYPE


def _handle_validate_return(value, values, key, callback, values_ns):
    values.update(vars(values_ns))
    if has_return_statement(callback):
        return value
    if key not in values:
        raise TypeError(f"Callback {callback} has no return statement and does not provide a value for {key}!")
    return values.get(key)


def _validate(cls, values, key, callback: Callable[..., Any]):
    # TODO: add defaults to values
    try:
        co_varnames = extract_var_names(callback)
        kwargs = {}
        kwargs.update(co_varnames)
        values_ns = SimpleNamespace(**values)
        kwargs.update({"cls": cls, "self": values_ns})
        kwargs = {
            key: value for key, value in kwargs.items() if key in co_varnames.keys() and value is not INSPECT_EMPTY_TYPE
        }
        kwargs.update({key: value for key, value in values.items() if key in co_varnames.keys()})
        if len(missing := [key for key in co_varnames.keys() if key not in kwargs.keys()]) > 1:
            raise TypeError(f"Some Arguments not provided by init dataclass values: {missing})")
        if len(missing) == 1:
            # in some cases co_var names does not contain the wrapped argument (e.g. `func`)
            return _handle_validate_return(callback(values.pop(key), **kwargs), values, key, callback, values_ns)
        return _handle_validate_return(callback(**kwargs), values, key, callback, values_ns)
    except TypeError as e:
        raise TypeError(f"Error while validating {key} for {cls.__class__.__name__}: {e}")


def _process_validator(self, values, validators: dict, **kwargs):
    return {key: _validate(self, values, key, callback) for key, callback in validators.items() if key in kwargs}


def _process_type_checking(dc_cls, validate=False, **kwargs):
    return {
        key: check_type(dataclass_fields(dc_cls).get(key).type, key, value, validate=validate)
        for key, value in kwargs.items()
        if key in dataclass_fields(dc_cls).keys()
    }


def check_dataclass_kwargs(dc_cls, validate=False, **kwargs) -> Dict[str, Any]:
    """Check dataclass types."""
    kwargs.update(_process_type_checking(dc_cls, **kwargs, validate=validate))
    return kwargs


def validate_dataclass_kwargs(dc_cls, validate=False, **kwargs):
    """Validate dataclass (includes type checks + validators)."""
    _validators = dataclass_validators(dc_cls)

    # append init values with the default values for init fields
    kwargs.update(
        {
            field.name: default(field)
            for field in dataclass_fields(dc_cls).values()
            if field.name not in kwargs and field.init
        }
    )

    if _validators and not validate:
        logging.warning(
            f"Validators are provided for attributes [{_validators.keys()}] in dataclass {dc_cls.__name__}, but validate is set to False!"
        )

    _required_keys = dataclass_required_keys(dc_cls)

    if is_eval_env(dc_cls):
        kwargs.update(get_env_vars(dc_cls))
    kwargs.update(_process_validator(dc_cls, kwargs, _validators, **kwargs))
    kwargs.update(_process_type_checking(dc_cls, **kwargs, validate=validate))
    if missing_keys := [key for key in _required_keys if key not in kwargs.keys()]:
        raise TypeError(f"Missing required values for keys {missing_keys} for dataclass {dc_cls.__name__}!")

    return kwargs
