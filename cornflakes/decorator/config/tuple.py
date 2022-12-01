from dataclasses import astuple, fields, is_dataclass
from typing import Any

from cornflakes.decorator.config._helper import tuple_factory


def to_tuple(self) -> Any:
    """Method to convert Dataclass with slots to dict."""
    if not is_dataclass(self):
        return self
    new_tuple = astuple(self, tuple_factory=tuple_factory(self))
    if not (
        isinstance(new_tuple, (list, tuple))
        or any([is_dataclass(f.type) or f.default_factory == list or isinstance(f.default, list) for f in dc_fields])
        if (dc_fields := fields(self))
        else True
    ):
        return new_tuple
    if isinstance(new_tuple, tuple):
        new_tuple = list(new_tuple)
    for idx, f in enumerate(dc_fields):
        if is_dataclass(value := getattr(self, f.name)):
            new_tuple[idx] = value.to_tuple()
        if isinstance(value, list):
            for sub_idx, sub_value in enumerate(value):
                if is_dataclass(sub_value):
                    value[sub_idx] = sub_value.to_tuple()
            new_tuple[idx] = value
    if isinstance(new_tuple, list):
        new_tuple = tuple(new_tuple)  # cast to tuple
    return new_tuple
