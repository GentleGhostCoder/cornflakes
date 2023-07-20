"""Top Level Module."""  # noqa: RST303 D205
from _cornflakes import apply_match, eval_csv, eval_datetime, eval_type, extract_between, ini_load
from cornflakes.builder import generate_config_module
from cornflakes.common import patch_module
from cornflakes.logging import attach_log, setup_logging
from cornflakes.parser import yaml_load

__author__ = "Semjon Geist"
__email__ = "semjon.geist@ionos.com"
__version__ = "3.3.8"  # <<FORCE_BUMP>>

__all__ = [
    "ini_load",
    "eval_type",
    "eval_datetime",
    "eval_csv",
    "extract_between",
    "apply_match",
    "generate_config_module",
    "yaml_load",
    "attach_log",
    "setup_logging",
    "patch_module",
]

patch_module("cornflakes")
