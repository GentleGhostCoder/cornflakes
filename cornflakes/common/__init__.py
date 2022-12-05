"""cornflakes common module.
__________________________________
"""  # noqa: RST303 D205
from cornflakes.common._extract_var_names import extract_var_names
from cornflakes.common._default_ca_path import default_ca_path
from cornflakes.common._type_to_str import type_to_str
from cornflakes.common._types import datetime_ms, unquoted_string
from cornflakes.common._patch_module import patch_module
from cornflakes.common._wrap_kwargs import wrap_kwargs

__all__ = [
    "default_ca_path",
    "type_to_str",
    "datetime_ms",
    "extract_var_names",
    "unquoted_string",
    "patch_module",
    "wrap_kwargs",
]

patch_module(globals())
