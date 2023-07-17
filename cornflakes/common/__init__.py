"""cornflakes common module.
__________________________________
"""  # noqa: RST303 D205
from cornflakes.common._check_type import check_type, get_actual_type
from cornflakes.common._default_ca_path import default_ca_path
from cornflakes.common._extract_var_names import extract_var_names
from cornflakes.common._patch_module import patch_module
from cornflakes.common._recursive_update import recursive_update
from cornflakes.common._type_to_str import type_to_str
from cornflakes.common._datetime_ms import datetime_ms
from cornflakes.common._unquoted_string import unquoted_string

__all__ = [
    "default_ca_path",
    "type_to_str",
    "extract_var_names",
    "patch_module",
    "check_type",
    "get_actual_type",
    "recursive_update",
    "datetime_ms",
    "unquoted_string",
]
