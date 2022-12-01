"""cornflakes config generation."""
from cornflakes.common import patch_module
from cornflakes.builder._generate_config_module import generate_group_module

__all__ = ["generate_group_module"]

patch_module(globals())
