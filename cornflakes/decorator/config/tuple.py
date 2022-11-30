from dataclasses import astuple, is_dataclass
from typing import Any


def to_tuple(self) -> Any:
    """Method to convert Dataclass with slots to dict."""
    if not is_dataclass(self):
        return self
    new_tuple = astuple(self, tuple_factory=getattr(self, "__tuple_factory__", tuple))
    if not any(
        [
            is_dataclass(value.type) or value.default_factory == list or isinstance(value.default, list)
            for value in getattr(self, "__dataclass_fields__", {}).values()
        ]
    ):
        return new_tuple
    if isinstance(new_tuple, tuple):
        new_tuple = list(new_tuple)
    for idx, key in enumerate(getattr(self, "__slots__", getattr(self, "__dict__", {}).keys())):
        if is_dataclass(value := getattr(self, key)):
            new_tuple[idx] = value.to_tuple()
        if isinstance(value, list):
            for sub_idx, sub_value in enumerate(value):
                if is_dataclass(sub_value):
                    value[sub_idx] = sub_value.to_tuple()
            new_tuple[idx] = value
    if isinstance(new_tuple, list):
        new_tuple = tuple(new_tuple)  # cast to tuple
    return new_tuple
