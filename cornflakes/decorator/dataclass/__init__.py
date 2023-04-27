"""custom dataclass wrapper."""
# from dataclasses import *  # noqa: F401, F403
from cornflakes.decorator.dataclass._dataclass import dataclass, to_dict, to_tuple
from cornflakes.decorator.dataclass._field import Field, field


__all__ = ["field", "dataclass", "Field", "to_dict", "to_tuple"]
