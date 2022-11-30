from dataclasses import astuple, is_dataclass
from typing import Any


def to_tuple(self) -> Any:
    """Method to convert Dataclass with slots to dict."""
    if not is_dataclass(self):
        return self
    new_tuple = astuple(self, tuple_factory=getattr(self, "__tuple_factory__", tuple))
    for idx, key in enumerate(getattr(self, "__slots__", getattr(self, "__dict__", {}).keys())):
        if is_dataclass(value := getattr(self, key)):
            new_tuple = list(new_tuple)
            new_tuple[idx] = to_tuple(value)
            new_tuple = tuple(new_tuple)
    return new_tuple
