"""Automatically generated Default Config.

!!!This files is autogenerated, please do not modify manually.!!!
!!!Change the file default-htw-logger.ini or the default values in the base-classes of htw_logger.config!!!
!!!IF htw_logger.config not exists run ```make install``` before!!!
"""
from dataclasses import field
from typing import List

from cornflakes import config_group
from tests.configs.sub_config import SubConfig


@config_group(files=["tests/configs/default.ini"])
class MainConfig:
    """Main config class of the module."""

    sub_config: List[SubConfig] = field(default_factory=list)


__all__ = ["MainConfig"]
