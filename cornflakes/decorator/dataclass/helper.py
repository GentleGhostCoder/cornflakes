"""Dataclass helper functions used by the custom dataclass decorator."""
from dataclasses import Field
import re
from typing import Dict, Optional, Union

from cornflakes.decorator.dataclass._field import Field as CField
from cornflakes.decorator.types import (
    MISSING_TYPE,
    WITHOUT_DEFAULT,
    Config,
    ConfigArgument,
    ConfigGroup,
    Constants,
    Dataclass,
    Loader,
)


def is_config(cls):
    """Method to return flag that class is a config class."""
    return hasattr(cls, Constants.config_decorator.SECTIONS)


def is_group(cls):
    """Method to return flag that class is a config group class."""
    return not is_config(cls) and hasattr(cls, Constants.config_decorator.FILES)


def config_files(cls) -> ConfigArgument:
    """Method to return class __config_files__."""
    return getattr(cls, Constants.config_decorator.FILES, [])


def dataclass_fields(cls: Union[Config, ConfigGroup, Dataclass]) -> Dict[str, Union[Field, CField]]:
    """Method to return dataclass fields."""
    return getattr(cls, Constants.dataclass_decorator.FIELDS, {})


def dict_factory(cls):
    """Method to return class __dict_factory__."""
    # dict_factory_method = getattr(cls, "__dict_factory__", dict)
    #
    # # check if any field in class is a memoryview type
    # if any([f.type == memoryview for f in dataclass_fields(cls).values()]):
    #     # if so, return a dict factory that converts memoryview to bytes
    #     def dict_factory_wrapper(obj):
    #         """Method to convert memoryview to bytes."""
    #         return dict_factory_method({k: bytes(v) if isinstance(v, memoryview) else v for k, v in obj})
    #
    #     return dict_factory_wrapper
    return getattr(cls, Constants.dataclass_decorator.DICT_FACTORY, dict)


def normalized_class_name(cls):
    """Method to return class name normalized."""
    return re.sub(r"([a-z])([A-Z])", "\\1_\\2", cls.__name__).lower()


def tuple_factory(cls):
    """Method to return class __tuple_factory__."""
    return getattr(cls, Constants.dataclass_decorator.TUPLE_FACTORY, tuple)


def is_config_list(cls):
    """Method to return flag that the object is a list of configs."""
    return getattr(cls, Constants.config_decorator.IS_LIST, False) or (
        hasattr(cls, "__args__") and getattr(cls.__args__[0], Constants.config_decorator.IS_LIST, False)
    )


def get_not_ignored_slots(cls):
    """Method to return slots that are not ignored fields."""
    return [
        slot
        for slot in getattr(cls, Constants.dataclass_decorator.FIELDS, {}).keys()
        if slot not in cls.__ignored_slots__
    ]


def is_use_regex(cls):
    """Method to return flag that the config class can be empty."""
    return getattr(cls, Constants.config_decorator.USE_REGEX, False)


def is_allow_empty(cls):
    """Method to return flag that the config class can be empty."""
    return getattr(cls, Constants.config_decorator.ALLOW_EMPTY, False)


def pass_section_name(cls):
    """Method to return flag that the config has section_name in slots, so that the section title is passed in."""
    return Constants.config_decorator.SECTION_NAME_KEY in getattr(cls, Constants.dataclass_decorator.FIELDS, {})


def dc_slot_missing_default(slot):
    """Checks if the dataclass has a default / default_factory."""
    return slot.default in (MISSING_TYPE, WITHOUT_DEFAULT) and slot.default_factory in (MISSING_TYPE, WITHOUT_DEFAULT)


def dc_slot_get_default(slot):
    """Method to get the default value of the dataclass."""
    return slot.default if slot.default not in (MISSING_TYPE, WITHOUT_DEFAULT) else slot.default_factory


def get_default_loader(files: Optional[list] = None):
    """Method to get the default loader from filenames."""
    return (
        Loader.DICT
        if not files
        else Loader.INI
        if files[0][-3:] == "ini"
        else Loader.YAML
        if files[0][-3:] == "yaml"
        else Loader.DICT
    )
