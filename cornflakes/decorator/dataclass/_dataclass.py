from dataclasses import dataclass as new_dataclass
from dataclasses import fields, is_dataclass
from typing import Any, Callable, Optional, Type, Union, cast

from cornflakes.decorator._add_dataclass_slots import add_slots
from cornflakes.decorator._indexer import is_index
from cornflakes.decorator.config.ini import to_ini, to_ini_bytes
from cornflakes.decorator.config.yaml import to_yaml, to_yaml_bytes
from cornflakes.decorator.dataclass._enforce_types import enforce_types as enforce
from cornflakes.decorator.dataclass._field import Field
from cornflakes.decorator.dataclass.helper import dict_factory as d_factory
from cornflakes.decorator.dataclass.helper import tuple_factory as t_factory
from cornflakes.decorator.types import DataclassProtocol


def _zero_copy_asdict_inner(obj, factory):
    """Patched version of dataclasses._asdict_inner that does not copy the dataclass values."""
    if is_dataclass(obj):
        result = []
        for f in fields(obj):
            value = _zero_copy_asdict_inner(getattr(obj, f.name), factory)
            result.append((f.name, value))
        return factory(result)
    elif isinstance(obj, tuple) and hasattr(obj, "_fields"):
        # obj is a namedtuple.  Recurse into it, but the returned
        # object is another namedtuple of the same type.  This is
        # similar to how other list- or tuple-derived classes are
        # treated (see below), but we just need to create them
        # differently because a namedtuple's __init__ needs to be
        # called differently (see bpo-34363).

        # I'm not using namedtuple's _asdict()
        # method, because:
        # - it does not recurse in to the namedtuple fields and
        #   convert them to dicts (using dict_factory).
        # - I don't actually want to return a dict here.  The main
        #   use case here is json.dumps, and it handles converting
        #   namedtuples to lists.  Admittedly we're losing some
        #   information here when we produce a json list instead of a
        #   dict.  Note that if we returned dicts here instead of
        #   namedtuples, we could no longer call asdict() on a data
        #   structure where a namedtuple was used as a dict key.

        return type(obj)(*[_zero_copy_asdict_inner(v, factory) for v in obj])
    elif isinstance(obj, (list, tuple)):
        # Assume we can create an object of this type by passing in a
        # generator (which is not true for namedtuples, handled
        # above).
        return type(obj)(_zero_copy_asdict_inner(v, factory) for v in obj)
    elif isinstance(obj, dict):
        return type(obj)(
            (_zero_copy_asdict_inner(k, factory), _zero_copy_asdict_inner(v, factory)) for k, v in obj.items()
        )
    else:
        return obj


def _zero_copy_astuple_inner(obj, factory):
    if is_dataclass(obj):
        result = []
        for f in fields(obj):
            value = _zero_copy_astuple_inner(getattr(obj, f.name), factory)
            result.append(value)
        return factory(result)
    elif isinstance(obj, tuple) and hasattr(obj, "_fields"):
        # obj is a namedtuple.  Recurse into it, but the returned
        # object is another namedtuple of the same type.  This is
        # similar to how other list- or tuple-derived classes are
        # treated (see below), but we just need to create them
        # differently because a namedtuple's __init__ needs to be
        # called differently (see bpo-34363).
        return type(obj)(*[_zero_copy_astuple_inner(v, factory) for v in obj])
    elif isinstance(obj, (list, tuple)):
        # Assume we can create an object of this type by passing in a
        # generator (which is not true for namedtuples, handled
        # above).
        return type(obj)(_zero_copy_astuple_inner(v, factory) for v in obj)
    elif isinstance(obj, dict):
        return type(obj)(
            (_zero_copy_astuple_inner(k, factory), _zero_copy_astuple_inner(v, factory)) for k, v in obj.items()
        )
    else:
        return obj


def _zero_copy_asdict(obj, *, factory=dict):
    """Custom version of dataclasses.asdict that does not copy the dataclass values."""
    if not is_dataclass(obj):
        raise TypeError("asdict() should be called on dataclass instances")
    return _zero_copy_asdict_inner(obj, factory)


def _zero_copy_astuple(obj, *, tuple_factory=tuple):
    """Custom version of dataclasses.astuple that does not copy the dataclass values."""
    if not is_dataclass(obj):
        raise TypeError("astuple() should be called on dataclass instances")
    return _zero_copy_astuple_inner(obj, tuple_factory)


def to_dict(self) -> Any:
    """Method to convert Dataclass with slots to dict."""
    if not is_dataclass(self):
        return self
    new_dict = _zero_copy_asdict(self, factory=d_factory(self))
    dc_fields = fields(self)
    if not (
        isinstance(new_dict, dict)
        or any([is_dataclass(f.type) or f.default_factory == list or isinstance(f.default, list) for f in dc_fields])
        if dc_fields
        else True
    ):
        return new_dict
    for f in dc_fields:
        if is_index(value := getattr(self, f.name)):
            type(value).reset()
            new_dict.update({f.name: value})
        if is_dataclass(value):
            new_dict.update({f.name: value.to_dict()})
        if isinstance(value, list) or isinstance(value, tuple):
            value = list(value)  # if tuple cast  to list
            for idx, sub_value in enumerate(value):
                if is_index(sub_value):
                    type(sub_value).reset()
                    value[idx] = sub_value
                if is_dataclass(sub_value):
                    value[idx] = sub_value.to_dict()
            new_dict.update({f.name: value})
    return new_dict


def to_tuple(self) -> Any:  # noqa: C901
    """Method to convert Dataclass with slots to dict."""
    if not is_dataclass(self):
        return self
    new_tuple = _zero_copy_astuple(self, tuple_factory=t_factory(self))
    dc_fields = fields(self)
    if not (
        isinstance(new_tuple, (list, tuple))
        or any([is_dataclass(f.type) or f.default_factory == list or isinstance(f.default, list) for f in dc_fields])
        if dc_fields
        else True
    ):
        return new_tuple
    if isinstance(new_tuple, tuple):
        new_tuple = list(new_tuple)
    for idx, f in enumerate(dc_fields):
        if is_index(value := getattr(self, f.name)):
            type(value).reset()
            new_tuple[idx] = value
        if is_dataclass(value):
            new_tuple[idx] = value.to_tuple()
        if isinstance(value, list):
            for sub_idx, sub_value in enumerate(value):
                if is_index(sub_value):
                    type(sub_value).reset()
                    value[sub_idx] = sub_value
                if is_dataclass(sub_value):
                    value[sub_idx] = sub_value.to_tuple()
            new_tuple[idx] = value
    if isinstance(new_tuple, list):
        new_tuple = tuple(new_tuple)  # cast to tuple
    return new_tuple


def dataclass(
    cls=None,
    dict_factory: Optional[Callable] = None,
    tuple_factory: Optional[Callable] = None,
    eval_env: bool = False,
    validate: bool = False,
    updatable: bool = False,
    **kwargs,
) -> Union[DataclassProtocol, Callable[..., DataclassProtocol], Any]:
    """Wrapper around built-in dataclasses dataclass."""

    def wrapper(w_cls: Type[Any]) -> Union[DataclassProtocol, Any]:
        dataclass_fields = {
            obj_name: getattr(w_cls, obj_name)
            for obj_name in dir(w_cls)
            if isinstance(getattr(w_cls, obj_name), Field) and hasattr(getattr(w_cls, obj_name), "alias")
        }
        has_add_slots = (
            kwargs.pop("slots", False)
            if "slots" in kwargs and "slots" not in new_dataclass.__code__.co_varnames
            else False
        )
        dc_cls: Union[DataclassProtocol, Any] = new_dataclass(w_cls, **kwargs)
        if has_add_slots:
            dc_cls = add_slots(dc_cls)
        dc_cls.__dataclass_fields__.update(dataclass_fields)
        dc_cls.__dict_factory__ = dict_factory or dict
        dc_cls.__tuple_factory__ = tuple_factory or tuple
        dc_cls.__eval_env__ = eval_env

        dc_cls.__ignored_slots__ = [f.name for f in fields(dc_cls) if getattr(f, "ignore", False)]

        dc_cls.to_dict = to_dict
        dc_cls.to_tuple = to_tuple
        dc_cls.to_ini = to_ini
        dc_cls.to_yaml = to_yaml
        dc_cls.to_yaml_bytes = to_yaml_bytes
        dc_cls.to_ini_bytes = to_ini_bytes

        if updatable and not kwargs.get("frozen", False):

            def _update(self, new):
                for key, value in new.items():
                    try:
                        setattr(self, key, value)
                    except AttributeError:
                        pass

            dc_cls.update = _update

        if validate:
            dc_cls = enforce(dc_cls, validate)
        return cast(DataclassProtocol, dc_cls)

    if cls:
        return wrapper(cls)
    return wrapper
