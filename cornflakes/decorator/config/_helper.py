from typing import Union

from cornflakes.decorator.config._protocols import Config, ConfigGroup


def is_config(cls: Config):
    """Method to return flag that class is a config class."""
    return hasattr(cls, "__config_sections__")


def is_group(cls):
    """Method to return flag that class is a config group class."""
    return not is_config(cls) and hasattr(cls, "__config_files__")


def is_config_list(cls: Config):
    """Method to return flag that the object is a list of configs."""
    return getattr(cls, "__config_list__", False) or (
        hasattr(cls, "__args__") and getattr(cls.__args__[0], "__config_list__", False)
    )


def get_config_slots(cls: Config):
    """Method to return slots that are not ignored fields."""
    return [slot for slot in getattr(cls, "__slots__", ()) if slot not in cls.__ignored_slots__]


def is_multi_config(cls: Union[Config, ConfigGroup]):
    """Method to return flag that the config class can be empty."""
    return getattr(cls, "__multi_config__", False)


def allow_empty(cls: Union[Config, ConfigGroup]):
    """Method to return flag that the config class can be empty."""
    return getattr(cls, "__allow_empty_config__", False)


def pass_section_name(cls: Config):
    """Method to return flag that the config has section_name in slots, so that the section title is passed in."""
    return "section_name" in cls.__dataclass_fields__.keys()
