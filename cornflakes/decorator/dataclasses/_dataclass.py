import contextlib
import dataclasses
from dataclasses import fields, is_dataclass
import sys
from typing import Any, Callable, Optional, Type, Union, overload

from typing_extensions import dataclass_transform  # type: ignore

from cornflakes.common import recursive_update
from cornflakes.decorator._indexer import is_index
from cornflakes.decorator.dataclasses._add_dataclass_slots import add_slots
from cornflakes.decorator.dataclasses._enforce_types import enforce_types
from cornflakes.decorator.dataclasses._field import Field, field
from cornflakes.decorator.dataclasses._helper import dict_factory as d_factory
from cornflakes.decorator.dataclasses._helper import tuple_factory as t_factory
from cornflakes.decorator.dataclasses._validate import check_dataclass_kwargs, validate_dataclass_kwargs
from cornflakes.types import _T, CornflakesDataclass


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


def to_tuple(self) -> Any:  # noqa: C901
    """Method to convert Dataclass with slots to dict."""
    if not is_dataclass(self):
        return self
    new_tuple = _zero_copy_astuple_inner(self, t_factory(self))
    dc_fields = fields(self)
    if not (
        isinstance(new_tuple, (list, tuple))
        or any(is_dataclass(f.type) or f.default_factory == list or isinstance(f.default, list) for f in dc_fields)
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


def _zero_copy_asdict_inner(obj):
    """Patched version of dataclasses._asdict_inner that does not copy the dataclass values."""
    # if hasattr(obj, "__dict__"):
    #     return obj.__dict__

    if is_dataclass(obj):
        result = []
        for f in fields(obj):
            value = _zero_copy_asdict_inner(getattr(obj, f.name))
            result.append((f.name, value))
        return result
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
        return type(obj)(*[_zero_copy_asdict_inner(v) for v in obj])
    elif isinstance(obj, (list, tuple)):
        # Assume we can create an object of this type by passing in a
        # generator (which is not true for namedtuples, handled
        # above).
        return type(obj)(_zero_copy_asdict_inner(v) for v in obj)
    elif isinstance(obj, dict):
        return type(obj)((_zero_copy_asdict_inner(k), _zero_copy_asdict_inner(v)) for k, v in obj.items())
    else:
        return obj


# @profile
def _to_dict(self) -> Union[tuple, dict, Any]:
    """Method to convert Dataclass with slots to dict."""
    if not is_dataclass(self):
        return self
    new_dict = d_factory(self)(_zero_copy_asdict_inner(self))
    dc_fields = fields(self)
    if not (
        isinstance(new_dict, dict)
        or any(is_dataclass(f.type) or f.default_factory == list or isinstance(f.default, list) for f in dc_fields)
        if dc_fields
        else True
    ):
        return new_dict
    for f in dc_fields:
        if is_index(value := getattr(self, f.name)):
            type(value).reset()
            new_dict.update({f.name: value})
        if is_dataclass(value):
            new_dict.update({f.name: _to_dict(value)})
        if isinstance(value, (list, tuple)):
            value = list(value)  # if tuple cast  to list
            for idx, sub_value in enumerate(value):
                if is_index(sub_value):
                    type(sub_value).reset()
                    value[idx] = sub_value
                if is_dataclass(sub_value):
                    value[idx] = _to_dict(sub_value)
            new_dict.update({f.name: value})
    return new_dict


def _new_getattr(self, key):
    value = object.__getattribute__(self, key)
    if is_index(value):
        type(value).reset()
        return value
    if is_dataclass(value):
        return _to_dict(value)
    if isinstance(value, (list, tuple)):
        value = list(value)  # if tuple cast  to list
        for idx, sub_value in enumerate(value):
            if is_index(sub_value):
                type(sub_value).reset()
                value[idx] = sub_value
            if is_dataclass(sub_value):
                value[idx] = _to_dict(sub_value)
        return value
    return value


def to_dict(self) -> dict:
    """Method to convert Dataclass with slots to dict."""
    return d_factory(self)(_to_dict(self))


if sys.version_info >= (3, 10):

    @dataclass_transform(field_specifiers=(field, Field))
    @overload
    def dataclass(
        *,
        init: bool = True,
        repr: bool = True,
        eq: bool = True,
        order: bool = False,
        unsafe_hash: bool = False,
        frozen: bool = False,
        kw_only: bool = False,
        slots: bool = False,
        match_args: bool = True,
        dict_factory: Optional[Callable] = None,
        tuple_factory: Optional[Callable] = None,
        eval_env: bool = False,
        validate: bool = False,
        updatable: bool = False,
        **kwargs: Any,
    ) -> Callable[[Type[_T]], Union[Type[CornflakesDataclass], Type[_T]]]:
        ...

    @dataclass_transform(field_specifiers=(field, Field))
    @overload
    def dataclass(
        _cls: Type[_T],
        /,
        *,
        init: bool = True,
        repr: bool = True,
        eq: bool = True,
        order: bool = False,
        unsafe_hash: bool = False,
        frozen: bool = False,
        kw_only: bool = False,
        slots: bool = False,
        match_args: bool = True,
        dict_factory: Optional[Callable] = None,
        tuple_factory: Optional[Callable] = None,
        eval_env: bool = False,
        validate: bool = False,
        updatable: bool = False,
        **kwargs: Any,
    ) -> Union[Type[CornflakesDataclass], Type[_T]]:
        ...

else:

    @dataclass_transform(field_specifiers=(field, Field))
    @overload
    def dataclass(
        *,
        init: bool = True,
        repr: bool = True,
        eq: bool = True,
        order: bool = False,
        unsafe_hash: bool = False,
        frozen: bool = False,
        dict_factory: Optional[Callable] = None,
        tuple_factory: Optional[Callable] = None,
        eval_env: bool = False,
        validate: bool = False,
        updatable: bool = False,
        **kwargs: Any,
    ) -> Callable[[Type[_T]], Union[Type[CornflakesDataclass], Type[_T]]]:
        ...

    @dataclass_transform(field_specifiers=(field, Field))
    @overload
    def dataclass(
        _cls: Type[_T],  # type: ignore
        /,
        *,
        init: bool = True,
        repr: bool = True,
        eq: bool = True,
        order: bool = False,
        unsafe_hash: bool = False,
        frozen: bool = False,
        dict_factory: Optional[Callable] = None,
        tuple_factory: Optional[Callable] = None,
        eval_env: bool = False,
        validate: bool = False,
        updatable: bool = False,
        **kwargs: Any,
    ) -> Union[Type[CornflakesDataclass], Type[_T]]:
        ...


@dataclass_transform(field_specifiers=(field, Field))
def dataclass(
    cls: Optional[Type[_T]] = None,
    /,
    *,
    init: bool = True,
    repr: bool = True,
    eq: bool = True,
    order: bool = False,
    unsafe_hash: bool = False,
    frozen: bool = False,
    kw_only: bool = False,
    slots: bool = False,
    match_args: bool = True,
    dict_factory: Optional[Callable] = None,
    tuple_factory: Optional[Callable] = None,
    eval_env: bool = False,
    validate: bool = False,
    updatable: bool = False,
    **kwargs: Any,
) -> Union[Callable[[Type[_T]], Union[Type[CornflakesDataclass], Type[_T]]], Type[CornflakesDataclass], Type[_T]]:
    """Wrapper around built-in dataclasses dataclass."""
    if sys.version_info >= (3, 10):
        kwargs = dict(kw_only=kw_only, slots=slots, match_args=match_args)
    else:
        kwargs: dict = {}

    def create_dataclass(w_cls: Type[_T]) -> Union[Type[CornflakesDataclass], Type[_T]]:
        """
        Create a Cornflakes dataclass from a regular dataclass.

        :param w_cls: The class to create the Cornflakes dataclass from.
        :type w_cls: type
        :returns: A Cornflakes dataclass.
        :rtype: type
        """
        dataclass_fields = {
            obj_name: getattr(w_cls, obj_name)
            for obj_name in dir(w_cls)
            if isinstance(getattr(w_cls, obj_name), Field) and hasattr(getattr(w_cls, obj_name), "aliases")
        }
        dc_cls = dataclasses.dataclass(  # type: ignore[call-overload]
            w_cls,
            init=init,
            repr=repr,
            eq=eq,
            order=order,
            unsafe_hash=unsafe_hash,
            frozen=frozen,
            **kwargs,
        )

        if slots and sys.version_info < (3, 10):
            dc_cls = add_slots(dc_cls)

        dc_cls.__dataclass_fields__.update(dataclass_fields)
        dc_cls.__dict_factory__ = dict_factory or dict
        dc_cls.__tuple_factory__ = tuple_factory or tuple
        dc_cls.__eval_env__ = eval_env

        dc_cls.__ignored_slots__ = [f.name for f in dataclasses.fields(dc_cls) if getattr(f, "ignore", False)]

        dc_cls.to_dict = to_dict
        dc_cls.to_tuple = to_tuple

        dc_cls.validate_kwargs = classmethod(validate_dataclass_kwargs)
        dc_cls.check_kwargs = classmethod(check_dataclass_kwargs)

        if updatable and not kwargs.get("frozen", False):

            def _update(self, new, merge_lists=False):
                for key, value in new.items():
                    with contextlib.suppress(AttributeError):
                        recursive_update(getattr(self, key), value, merge_lists=merge_lists)

            dc_cls.update = _update

        if validate:
            dc_cls = enforce_types(dc_cls, validate=validate)

        dc_cls.__doc__ = w_cls.__doc__
        dc_cls.__module__ = w_cls.__module__
        dc_cls.__qualname__ = w_cls.__qualname__
        dc_cls.__init__.__doc__ = w_cls.__init__.__doc__
        dc_cls.__getitem__ = _new_getattr

        static_keys = [f.name for f in dataclasses.fields(dc_cls) if not getattr(f, "ignore", False)]

        def keys(self):
            return static_keys

        dc_cls.keys = keys

        return dc_cls

    return create_dataclass(cls) if cls else create_dataclass  # type: ignore
