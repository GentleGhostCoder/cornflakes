"""Dataclass helper functions used by the custom dataclass decorator."""
import dataclasses
from dataclasses import fields as dc_fields
from os import environ
import re

from _cornflakes import eval_type

from cornflakes.types import MISSING_TYPE, WITHOUT_DEFAULT_TYPE, Constants


def is_config(cls):
    """Method to return flag that class is a config class."""
    return hasattr(cls, Constants.config_decorator.SECTIONS)


def is_group(cls):
    """Method to return flag that class is a config group class."""
    return not is_config(cls) and hasattr(cls, Constants.config_decorator.FILES)


def config_files(cls):
    """Method to return class __config_files__."""
    return getattr(cls, Constants.config_decorator.FILES, [])


def config_sections(cls):
    """Method to return class __config_sections__."""
    return getattr(cls, Constants.config_decorator.SECTIONS, [])


def dataclass_fields(cls):
    """Method to return dataclass fields."""
    return getattr(cls, Constants.dataclass_decorator.FIELDS, {})


def dataclass_validators(cls):
    """Method to return dataclass validators."""
    return getattr(cls, Constants.dataclass_decorator.VALIDATORS, {})


def dataclass_required_keys(cls):
    """Method to return dataclass required keys."""
    return getattr(cls, Constants.dataclass_decorator.REQUIRED_KEYS, {})


def is_eval_env(cls):
    """Method to return flag that class is a eval env class."""
    return getattr(cls, Constants.dataclass_decorator.EVAL_ENV, False)


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
    return isinstance(slot.default, WITHOUT_DEFAULT_TYPE) or isinstance(slot.default_factory, WITHOUT_DEFAULT_TYPE)


def default(slot):
    """Method to get the default value of the dataclass."""
    return slot.default_factory if isinstance(slot.default, (MISSING_TYPE, WITHOUT_DEFAULT_TYPE)) else slot.default


def get_env_vars(dc_cls):
    """Method to get the environment variables for the dataclass."""
    return {key: eval_type(environ[key]) for key in dc_cls.__dataclass_fields__.keys() if key in environ.keys()}


def fields(class_or_instance):
    """Patched method of the dataclasses fields method to ignore the custom dataclass."""
    return dc_fields(class_or_instance)


dataclasses.fields = fields
