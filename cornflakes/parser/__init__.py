"""Cornflakes config parser module."""
from cornflakes.common import patch_module
from cornflakes.parser._yaml import yaml_load

__all__ = ["yaml_load"]

patch_module(globals())
