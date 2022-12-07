"""cornflakes (Top-level package).
____________________________________
"""  # noqa: RST303 D205
from _cornflakes import apply_match, eval_csv, eval_datetime, eval_type, extract_between, ini_load

from cornflakes.common import patch_module
from cornflakes.decorator import config, config_group, add_slots, click_cli, Loader, dataclass, field, config_field
from cornflakes.decorator.dataclass.validator import AnyUrl
from cornflakes.builder import generate_group_module
from cornflakes.parser import yaml_load
from cornflakes.logging import attach_log, setup_logging

__author__ = "Semjon Geist"
__email__ = "semjon.geist@ionos.com"
__version__ = "3.0.9"  # <<COOKIETEMPLE_FORCE_BUMP>>

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
    "AnyUrl",
    "add_slots",
    "generate_group_module",
    "yaml_load",
    "attach_log",
    "setup_logging",
    "Loader",
    "patch_module",
    "dataclass",
    "field",
    "config_field",
]

patch_module(globals())
