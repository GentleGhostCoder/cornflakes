import dataclasses
from dataclasses import dataclass as new_dataclass
from dataclasses import fields, is_dataclass
from typing import Any, Callable, Optional, Type, Union, cast

from cornflakes.decorator._add_dataclass_slots import add_slots
from cornflakes.decorator.config.dict import to_dict
from cornflakes.decorator.config.ini import to_ini, to_ini_bytes
from cornflakes.decorator.config.tuple import to_tuple
from cornflakes.decorator.config.yaml import to_yaml, to_yaml_bytes
from cornflakes.decorator.dataclass._enforce_types import enforce_types as enforce
from cornflakes.decorator.dataclass._field import Field
from cornflakes.decorator.types import DataclassProtocol


def _zero_copy_asdict_inner(obj, dict_factory):
    """Patched version of dataclasses._asdict_inner that does not copy the dataclass values."""
    if is_dataclass(obj):
        result = []
        for f in fields(obj):
            value = _zero_copy_asdict_inner(getattr(obj, f.name), dict_factory)
            result.append((f.name, value))
        return dict_factory(result)
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

        return type(obj)(*[_zero_copy_asdict_inner(v, dict_factory) for v in obj])
    elif isinstance(obj, (list, tuple)):
        # Assume we can create an object of this type by passing in a
        # generator (which is not true for namedtuples, handled
        # above).
        return type(obj)(_zero_copy_asdict_inner(v, dict_factory) for v in obj)
    elif isinstance(obj, dict):
        return type(obj)(
            (_zero_copy_asdict_inner(k, dict_factory), _zero_copy_asdict_inner(v, dict_factory)) for k, v in obj.items()
        )
    else:
        return obj


def _zero_copy_astuple_inner(obj, tuple_factory):
    if is_dataclass(obj):
        result = []
        for f in fields(obj):
            value = _zero_copy_astuple_inner(getattr(obj, f.name), tuple_factory)
            result.append(value)
        return tuple_factory(result)
    elif isinstance(obj, tuple) and hasattr(obj, "_fields"):
        # obj is a namedtuple.  Recurse into it, but the returned
        # object is another namedtuple of the same type.  This is
        # similar to how other list- or tuple-derived classes are
        # treated (see below), but we just need to create them
        # differently because a namedtuple's __init__ needs to be
        # called differently (see bpo-34363).
        return type(obj)(*[_zero_copy_astuple_inner(v, tuple_factory) for v in obj])
    elif isinstance(obj, (list, tuple)):
        # Assume we can create an object of this type by passing in a
        # generator (which is not true for namedtuples, handled
        # above).
        return type(obj)(_zero_copy_astuple_inner(v, tuple_factory) for v in obj)
    elif isinstance(obj, dict):
        return type(obj)(
            (_zero_copy_astuple_inner(k, tuple_factory), _zero_copy_astuple_inner(v, tuple_factory))
            for k, v in obj.items()
        )
    else:
        return obj


DATACLASS_PATCHED = False


def patch_dataclasses():
    if not DATACLASS_PATCHED:
        setattr(dataclasses, "_asdict_inner", _zero_copy_asdict_inner)
        setattr(dataclasses, "_astuple_inner", _zero_copy_astuple_inner)


def dataclass(
    cls=None,
    dict_factory: Optional[Callable] = None,
    tuple_factory: Optional[Callable] = None,
    eval_env: bool = False,
    validate: bool = False,
    updatable: bool = False,
    **kwargs
) -> Union[DataclassProtocol, Callable[..., DataclassProtocol], Any]:
    """Wrapper around built-in dataclasses dataclass."""

    patch_dataclasses()

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
