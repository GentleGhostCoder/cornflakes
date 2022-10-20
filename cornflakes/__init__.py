"""cornflakes (Top-level package).
__________________________________

.. currentmodule:: cornflakes

.. autosummary::
   :toctree: _generate

    ini_load
    eval_type
    eval_datetime
    eval_csv
    extract_between
    apply_match
    ni_config
    ini_group
    dd_slots
    generate_ini_group_module
    make_cli
"""  # noqa: RST303 D205
from _cornflakes import apply_match, eval_csv, eval_datetime, eval_type, extract_between, ini_load
from cornflakes.decorator import ini_config, ini_group, add_slots
from cornflakes.config import generate_ini_group_module
from cornflakes.click import make_cli

__author__ = "Semjon Geist"
__email__ = "semjon.geist@ionos.com"
__version__ = "2.5.4"

__all__ = [
    "ini_load",
    "eval_type",
    "eval_datetime",
    "eval_csv",
    "extract_between",
    "apply_match",
    "ini_config",
    "ini_group",
    "add_slots",
    "generate_ini_group_module",
    "make_cli",
]
