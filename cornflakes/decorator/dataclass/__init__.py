"""custom dataclass wrapper."""
# from dataclasses import *  # noqa: F401, F403
from cornflakes.decorator.dataclass._dataclass import dataclass, to_dict, to_tuple
from cornflakes.decorator.dataclass._field import Field, field
from cornflakes.decorator.dataclass._validate import check_dataclass_kwargs


__all__ = ["field", "dataclass", "Field", "to_dict", "to_tuple", "check_dataclass_kwargs"]
