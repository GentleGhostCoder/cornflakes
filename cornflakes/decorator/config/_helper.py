import re
from typing import Any, Optional, Union

from cornflakes.decorator._types import Config, ConfigArgument, ConfigGroup, DataclassProtocol, Loader


def is_config(cls):
    """Method to return flag that class is a config class."""
    return hasattr(cls, "__config_sections__")


def is_group(cls):
    """Method to return flag that class is a config group class."""
    return not is_config(cls) and hasattr(cls, "__config_files__")


def config_files(cls) -> ConfigArgument:
    """Method to return class __config_files__."""
    return getattr(cls, "__config_files__", [])


def dataclass_fields(cls: Union[Config, ConfigGroup, DataclassProtocol]) -> dict:
    """Method to return dataclass fields."""
    return getattr(cls, "__dataclass_fields__", {})


def dict_factory(cls: Union[Config, ConfigGroup, DataclassProtocol]) -> Any:
    """Method to return class __dict_factory__."""
    return getattr(cls, "__dict_factory__", dict)


def normalized_class_name(cls):
    """Method to return class name normalized."""
    return re.sub(r"([a-z])([A-Z])", "\\1_\\2", cls.__name__).lower()


def tuple_factory(cls: Union[Config, ConfigGroup, DataclassProtocol]) -> Any:
    """Method to return class __tuple_factory__."""
    return getattr(cls, "__tuple_factory__", tuple)


def is_config_list(cls):
    """Method to return flag that the object is a list of configs."""
    return getattr(cls, "__config_list__", False) or (
        hasattr(cls, "__args__") and getattr(cls.__args__[0], "__config_list__", False)
    )


def get_not_ignored_slots(cls):
    """Method to return slots that are not ignored fields."""
    return [slot for slot in getattr(cls, "__dataclass_fields__", {}).keys() if slot not in cls.__ignored_slots__]


def is_multi_config(cls):
    """Method to return flag that the config class can be empty."""
    return getattr(cls, "__multi_config__", False)


def is_allow_empty(cls):
    """Method to return flag that the config class can be empty."""
    return getattr(cls, "__allow_empty_config__", False)


def pass_section_name(cls):
    """Method to return flag that the config has section_name in slots, so that the section title is passed in."""
    return "section_name" in cls.__dataclass_fields__.keys()


def get_default_loader(files: Optional[list] = None):
    """Method to get the default loader from filenames."""
    return (
        Loader.DICT_LOADER
        if not files
        else Loader.INI_LOADER
        if files[0][-3:] == "ini"
        else Loader.YAML_LOADER
        if files[0][-3:] == "yaml"
        else Loader.DICT_LOADER
    )
