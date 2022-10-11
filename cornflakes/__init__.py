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
"""  # noqa: RST303 D205
from _cornflakes import apply_match, eval_csv, eval_datetime, eval_type, extract_between, ini_load
from cornflakes.common import default_ca_path
from cornflakes.common import DatetimeMS, datetime_ms

__author__ = "Semjon Geist"
__email__ = "semjon.geist@ionos.com"
__version__ = "1.5.5"

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
]
