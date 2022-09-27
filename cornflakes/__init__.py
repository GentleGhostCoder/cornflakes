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

__author__ = "Semjon Geist"
__email__ = "semjon.geist@ionos.com"
__version__ = "1.4.4"

from _cornflakes import apply_match, eval_csv, eval_datetime, eval_type, extract_between, ini_load
from cornflakes._default_ca_path import default_ca_path
from cornflakes._types import DatetimeMS, datetime_ms

# static definition for reference to
# ini_load = None
# eval_type = None
# eval_datetime = None
# eval_csv = None
# extract_between = None
# apply_match = None
# simple_hmac = None
# simple_sha256 = None

# dynamic load of pybind11 modules to create better docs
# pybind11_modules = [str(key) for key in _cornflakes.__dict__.keys() if re.match("[a-z].*", key)]
# for func_name in pybind11_modules:
#     _func = _cornflakes.__dict__.get(func_name)
#     func = None
#     ref_str = f"_cornflakes.{func_name}"
#     docs = _func.__doc__.split("\n")
#     args_str = ",".join(
#         [value.split(":")[0] for value in _func.__doc__.split("\n")[0].split("(")[1].split(")")[0].split(",")]
#     )
#     exec(  # noqa: S102
#         f"""
# def {docs[0]}:
#      '''reference of :meth:`{ref_str}`'''
#      return _cornflakes.__dict__.get("{func_name}")({args_str})
#     """,
#         locals(),
#     )


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
    "simple_hmac",
    "simple_sha256",
]
