import contextlib
import dataclasses
from dataclasses import fields, is_dataclass
import sys
from typing import Any, Callable, Optional, Type, Union, overload

from typing_extensions import dataclass_transform  # type: ignore

from cornflakes.common import recursive_update
from cornflakes.decorator.dataclasses._add_dataclass_slots import add_slots
from cornflakes.decorator.dataclasses._enforce_types import enforce_types
from cornflakes.decorator.dataclasses._field import Field, field
from cornflakes.decorator.dataclasses._helper import dc_field_without_default
from cornflakes.decorator.dataclasses._helper import dict_factory as d_factory
from cornflakes.decorator.dataclasses._helper import is_index
from cornflakes.decorator.dataclasses._helper import tuple_factory as t_factory
from cornflakes.decorator.dataclasses._helper import value_factory as v_factory
from cornflakes.decorator.dataclasses._validate import check_dataclass_kwargs, validate_dataclass_kwargs
from cornflakes.types import _T, Constants, CornflakesDataclass, MappingWrapper

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
        value_factory: Optional[Callable] = None,
        eval_env: bool = False,
        validate: bool = False,
        updatable: bool = False,
        ignore_none: bool = False,
        **kwargs: Any,
    ) -> Callable[[Type[_T]], Union[Type[CornflakesDataclass], MappingWrapper[_T]]]:
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
        value_factory: Optional[Callable] = None,
        eval_env: bool = False,
        validate: bool = False,
        updatable: bool = False,
        ignore_none: bool = False,
        **kwargs: Any,
    ) -> Union[Type[CornflakesDataclass], MappingWrapper[_T]]:
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
        value_factory: Optional[Callable] = None,
        eval_env: bool = False,
        validate: bool = False,
        updatable: bool = False,
        ignore_none: bool = False,
        **kwargs: Any,
    ) -> Callable[[Type[_T]], Union[Type[CornflakesDataclass], MappingWrapper[_T]]]:
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
        value_factory: Optional[Callable] = None,
        eval_env: bool = False,
        validate: bool = False,
        updatable: bool = False,
        ignore_none: bool = False,
        **kwargs: Any,
    ) -> Union[Type[CornflakesDataclass], MappingWrapper[_T]]:
        ...


# @dataclass_transform(field_specifiers=(field, Field))
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
    value_factory: Optional[Callable] = None,
    eval_env: bool = False,
    validate: bool = False,
    updatable: bool = False,
    ignore_none: bool = False,
    **kwargs: Any,
) -> Union[
    Callable[[Type[_T]], Union[Type[CornflakesDataclass], MappingWrapper[_T]]],
    Type[CornflakesDataclass],
    MappingWrapper[_T],
]:
    """Wrapper around built-in dataclasses dataclass."""
    if sys.version_info >= (3, 10):
        kwargs = dict(kw_only=kw_only, slots=slots, match_args=match_args)
    else:
        kwargs = {}

    def create_dataclass(w_cls: Type[_T]) -> Union[Type[CornflakesDataclass], MappingWrapper[_T]]:
        """
        Create a Cornflakes dataclass from a regular dataclass.

        :param w_cls: The class to create the Cornflakes dataclass from.
        :type w_cls: type
        :returns: A Cornflakes dataclass.
        :rtype: type
        """
        if not init and slots:
            # this is not supported by dataclasses
            raise AttributeError("Cannot specify both init=False and slots=True")

        dc_cls = _wrap_custom_dataclass(
            w_cls,
            init=init,
            repr=repr,
            eq=eq,
            order=order,
            unsafe_hash=unsafe_hash,
            frozen=frozen,
            dict_factory=dict_factory,
            tuple_factory=tuple_factory,
            value_factory=value_factory,
            eval_env=eval_env,
            **kwargs,
        )

        if slots and sys.version_info < (3, 10):
            dc_cls = add_slots(dc_cls)

        if updatable:
            if kwargs.get("frozen", False):
                raise AttributeError("Cannot set both frozen=True and updatable=True")

            def _update(self, new, merge_lists=False):
                current = {**self}
                with contextlib.suppress(AttributeError):
                    recursive_update(current, new, merge_lists=merge_lists)
                return type(self)(**current)

            dc_cls.update = _update

        if validate:
            dc_cls = enforce_types(dc_cls)

        dc_cls.__doc__ = w_cls.__doc__
        dc_cls.__module__ = w_cls.__module__
        dc_cls.__qualname__ = w_cls.__qualname__

        dc_cls = _wrap_mapping(dc_cls, ignore_none)

        return dc_cls

    return create_dataclass(cls) if cls else create_dataclass  # type: ignore


def _zero_copy_astuple_inner(obj, value_factory=None):
    if is_dataclass(obj):
        result = []
        for f in fields(obj):
            value = _zero_copy_astuple_inner(getattr(obj, f.name), v_factory(obj))
            result.append(value)
        return t_factory(obj)(result)
    if is_index(obj):
        type(obj).reset()
        return obj
    elif isinstance(obj, tuple) and hasattr(obj, "_fields"):
        # obj is a namedtuple.  Recurse into it, but the returned
        # object is another namedtuple of the same type.  This is
        # similar to how other list- or tuple-derived classes are
        # treated (see below), but we just need to create them
        # differently because a namedtuple's __init__ needs to be
        # called differently (see bpo-34363).
        return type(obj)(*[_zero_copy_astuple_inner(v) for v in obj])
    elif isinstance(obj, (list, tuple)):
        # Assume we can create an object of this type by passing in a
        # generator (which is not true for namedtuples, handled
        # above).
        return type(obj)(_zero_copy_astuple_inner(v) for v in obj)
    elif isinstance(obj, dict):
        return type(obj)((_zero_copy_astuple_inner(k), _zero_copy_astuple_inner(v)) for k, v in obj.items())
    else:
        return value_factory(obj) if value_factory else obj


def to_tuple(self) -> Any:  # noqa: C901
    """Method to convert Dataclass with slots to dict."""
    return _zero_copy_astuple_inner(self)


def _zero_copy_asdict_inner(obj, value_factory=None):
    """Patched version of dataclasses._asdict_inner that does not copy the dataclass values."""
    if is_dataclass(obj):
        result = []
        for f in fields(obj):
            value = _zero_copy_asdict_inner(getattr(obj, f.name), v_factory(obj))
            result.append((f.name, value))
        return d_factory(obj)(result)
    if is_index(obj):
        type(obj).reset()
        return obj
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
        return value_factory(obj) if value_factory else obj


# @profile
def to_dict(self) -> dict:
    """Method to convert Dataclass with slots to dict."""
    return _zero_copy_asdict_inner(self)


def _new_getattr_dict(self, key: str):
    return _zero_copy_asdict_inner(getattr(self, key), v_factory(self))


def _new_getattr_tuple(self, index: int):
    return _zero_copy_astuple_inner(getattr(self, self.keys()[index]), v_factory(self))


def _new_getattr(self, index):
    if isinstance(index, int):
        return _new_getattr_tuple(self, index)

    return _new_getattr_dict(self, index)


def _wrap_custom_dataclass(
    w_cls,
    init: bool = True,
    repr: bool = True,
    eq: bool = True,
    order: bool = False,
    unsafe_hash: bool = False,
    frozen: bool = False,
    dict_factory: Optional[Callable] = None,
    tuple_factory: Optional[Callable] = None,
    value_factory: Optional[Callable] = None,
    eval_env: bool = False,
    **kwargs: Any,
):
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

    dict_factory = staticmethod(dict_factory) if callable(dict_factory) else dict  # type: ignore
    tuple_factory = staticmethod(tuple_factory) if callable(tuple_factory) else tuple  # type: ignore
    value_factory = staticmethod(value_factory) if callable(value_factory) else None  # type: ignore

    dataclass_fields = {
        obj_name: getattr(w_cls, obj_name)
        for obj_name in dir(w_cls)
        if isinstance(getattr(w_cls, obj_name), Field) and hasattr(getattr(w_cls, obj_name), "aliases")
    }

    dc_cls.__dataclass_fields__.update(dataclass_fields)
    setattr(dc_cls, Constants.dataclass_decorator.EVAL_ENV, eval_env)
    setattr(dc_cls, Constants.dataclass_decorator.DICT_FACTORY, dict_factory)  # type: ignore
    setattr(dc_cls, Constants.dataclass_decorator.TUPLE_FACTORY, tuple_factory)  # type: ignore
    setattr(dc_cls, Constants.dataclass_decorator.VALUE_FACTORY, value_factory)  # type: ignore

    # Non-comparable fields should be compared via repr, so they are stored for later use
    setattr(
        dc_cls,
        Constants.dataclass_decorator.IGNORED_SLOTS,
        [f.name for f in dataclasses.fields(dc_cls) if getattr(f, "ignore", False)],
    )
    # setattr(dc_cls, Constants.dataclass_decorator.IGNORE_NONE, ignore_none)
    setattr(
        dc_cls,
        Constants.dataclass_decorator.VALIDATORS,
        {
            key: validator
            for key, value in dc_cls.__dataclass_fields__.items()
            if callable(validator := getattr(value, "validator", key))
        },
    )
    setattr(
        dc_cls,
        Constants.dataclass_decorator.REQUIRED_KEYS,
        [key for key, slot in dc_cls.__dataclass_fields__.items() if dc_field_without_default(slot)],
    )

    setattr(
        dc_cls,
        Constants.dataclass_decorator.INIT_EXCLUDE_KEYS,
        [key for key, slot in dc_cls.__dataclass_fields__.items() if not getattr(slot, "init", True)],
    )

    dc_cls.to_dict = to_dict
    dc_cls.to_tuple = to_tuple

    dc_cls.validate_kwargs = classmethod(validate_dataclass_kwargs)
    dc_cls.check_kwargs = classmethod(check_dataclass_kwargs)

    return dc_cls


def _wrap_mapping(dc_cls, ignore_none):
    """Wrap a mapping class."""

    dc_cls.__getitem__ = _new_getattr
    static_keys = [f.name for f in dataclasses.fields(dc_cls) if not getattr(f, "ignore", False)]
    if not ignore_none:

        def keys(_):
            return static_keys  #

        def _len(_):
            return len(static_keys)

        dc_cls.__len__ = classmethod(_len)
        dc_cls.keys = classmethod(keys)
    else:

        def keys(self):
            return [key for key in static_keys if getattr(self, key) is not None]

        def _len(self):
            return len(keys(self))

        dc_cls.keys = keys  # not classmethod
        dc_cls.__len__ = _len

    return dc_cls
