"""cornflakes (Top-level package).
____________________________________

.. currentmodule:: cornflakes

.. autosummary::
   :toctree: _generate

    ini_load
    eval_type
    eval_datetime
    eval_csv
    extract_between
    apply_match
    config
    config_group
    add_slots
    generate_group_module
    make_cli
    yaml_load
"""  # noqa: RST303 D205
from _cornflakes import apply_match, eval_csv, eval_datetime, eval_type, extract_between, ini_load
from cornflakes.decorator import config, config_group, add_slots
from cornflakes.builder import generate_group_module
from cornflakes.click import make_cli
from cornflakes.parser import yaml_load

__author__ = "Semjon Geist"
__email__ = "semjon.geist@ionos.com"
__version__ = "2.6.0"

__all__ = [
    "ini_load",
    "eval_type",
    "eval_datetime",
    "eval_csv",
    "extract_between",
    "apply_match",
    "config",
    "config_group",
    "add_slots",
    "generate_group_module",
    "make_cli",
    "yaml_load",
]
