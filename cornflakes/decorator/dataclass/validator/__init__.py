"""cornflakes default validators for config_fields."""
from cornflakes.common import patch_module
from cornflakes.decorator.dataclass.validator.url import AnyUrl

__all__ = ["AnyUrl"]

patch_module(globals())
