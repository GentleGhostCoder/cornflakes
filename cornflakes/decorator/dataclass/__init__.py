"""custom dataclass wrapper."""
# from dataclasses import *  # noqa: F401, F403
from cornflakes.common import patch_module
from cornflakes.decorator.dataclass._dataclass import dataclass
from cornflakes.decorator.dataclass._field import field, Field

__all__ = ["field", "dataclass", "Field"]

patch_module(globals())
