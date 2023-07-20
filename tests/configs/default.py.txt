"""Automatically generated Default Config."""
from typing import List

from cornflakes.decorator import field
from cornflakes.decorator.dataclasses import config_group
from tests.configs.sub_config import SubConfigClass


@config_group(files="tests/configs/default.ini", eval_env=True)
class MainConfig:
    """Main config class of the module."""

    sub_config_class: List[SubConfigClass] = field(default_factory=list)


__all__ = ["MainConfig"]
