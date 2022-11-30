"""cornflakes (Top-level package).
____________________________________

.. currentmodule:: cornflakes

.. autosummary::
   :toctree: _generate

"""  # noqa: RST303 D205
from _cornflakes import apply_match, eval_csv, eval_datetime, eval_type, extract_between, ini_load
from cornflakes.decorator import config, config_group, config_field, add_slots, click_cli, Loader
from cornflakes.decorator.dataclass.validator import AnyUrl
from cornflakes.builder import generate_group_module
from cornflakes.parser import yaml_load
from cornflakes.logging import attach_log, setup_logging

__author__ = "Semjon Geist"
__email__ = "semjon.geist@ionos.com"
__version__ = "3.0.3"

__all__ = [
    "click_cli",
    "ini_load",
    "eval_type",
    "eval_datetime",
    "eval_csv",
    "extract_between",
    "apply_match",
    "config",
    "config_group",
    "config_field",
    "AnyUrl",
    "add_slots",
    "generate_group_module",
    "yaml_load",
    "attach_log",
    "setup_logging",
    "Loader",
]

__doc__ = f"""{__doc__}
.. autosummary::
   :toctree: _generate

    {'''
    '''.join(__all__)}
"""
