from dataclasses import dataclass as new_dataclass
from dataclasses import fields
from typing import Any, Callable, Optional, Type, Union

from cornflakes.decorator._add_dataclass_slots import add_slots
from cornflakes.decorator._types import DataclassProtocol
from cornflakes.decorator.config.dict import to_dict
from cornflakes.decorator.config.ini import to_ini, to_ini_bytes
from cornflakes.decorator.config.tuple import to_tuple
from cornflakes.decorator.config.yaml import to_yaml, to_yaml_bytes
from cornflakes.decorator.dataclass._enforce_types import enforce_types as enforce
from cornflakes.decorator.dataclass._field import Field


def dataclass(
    cls=None,
    dict_factory: Optional[Callable] = None,
    tuple_factory: Optional[Callable] = None,
    eval_env: bool = False,
    validate: bool = False,
    **kwargs
) -> Union[DataclassProtocol, Callable[..., DataclassProtocol]]:
    """Wrapper around built-in dataclasses dataclass."""

    def wrapper(w_cls: Type[Any]) -> DataclassProtocol:
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

        if validate:
            dc_cls = enforce(dc_cls, validate)
        return dc_cls

    if cls:
        return wrapper(cls)
    return wrapper
