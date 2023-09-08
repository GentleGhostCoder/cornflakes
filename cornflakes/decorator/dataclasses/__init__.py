"""custom dataclass wrapper."""
from cornflakes.decorator.dataclasses._config import config_group, config, to_ini, to_yaml
from cornflakes.decorator.dataclasses._add_dataclass_slots import add_slots

# from dataclasses import *  # noqa: F401, F403
from cornflakes.decorator.dataclasses._dataclass import dataclass, to_dict, to_tuple
from cornflakes.decorator.dataclasses._field import Field, field
from cornflakes.decorator.dataclasses._helper import (
    is_config,
    is_group,
    normalized_class_name,
    config_files,
    default,
    dc_field_without_default,
    dataclass_fields,
    fields,
)
from cornflakes.decorator.dataclasses._validate import check_dataclass_kwargs, validate_dataclass_kwargs
from cornflakes.decorator.dataclasses.validator import AnyUrl

__all__ = [
    "add_slots",
    "field",
    "dataclass",
    "Field",
    "to_dict",
    "to_tuple",
    "validate_dataclass_kwargs",
    "check_dataclass_kwargs",
    "fields",
    "is_config",
    "is_group",
    "normalized_class_name",
    "config_files",
    "dataclass_fields",
    "default",
    "dc_field_without_default",
    "config",
    "config_group",
    "AnyUrl",
    "to_ini",
    "to_yaml",
    "fields",
]
