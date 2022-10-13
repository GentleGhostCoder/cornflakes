"""cornflakes (Top-level package).
__________________________________

.. currentmodule:: cornflakes

.. autosummary::
   :toctree: _generate

    default_ca_path
    datetime_ms
    ini_load
    eval_type
    eval_datetime
    eval_csv
    extract_between
    apply_match
    add_slots
    generate_default_config_py
    ini_config
"""  # noqa: RST303 D205
from _cornflakes import apply_match, eval_csv, eval_datetime, eval_type, extract_between, ini_load
from cornflakes._default_ca_path import default_ca_path
from cornflakes._types import DatetimeMS, datetime_ms
from cornflakes._add_dataclass_slots import add_slots
from cornflakes.config import generate_default_config_py
from cornflakes.decorator import ini_config

__author__ = "Semjon Geist"
__email__ = "semjon.geist@ionos.com"
__version__ = "2.1.8"

__all__ = [
    "datetime_ms",
    "DatetimeMS",
    "default_ca_path",
    "ini_load",
    "eval_type",
    "eval_datetime",
    "eval_csv",
    "extract_between",
    "apply_match",
    "add_slots",
    "ini_config",
    "generate_default_config_py",
]
