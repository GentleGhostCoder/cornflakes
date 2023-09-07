"""Dataclass helper functions used by the custom dataclass decorator."""
import dataclasses
from dataclasses import fields as dc_fields
from os import environ
import re
from typing import List, Optional

from cornflakes import eval_type, ini_load
from cornflakes.parser import yaml_load
from cornflakes.types import MISSING_TYPE, WITHOUT_DEFAULT_TYPE, Constants, IndexInstance, Loader


def is_index(obj):
    """Returns True if the given object is an index type."""
    return getattr(getattr(obj, "__class__", {}), "__name__", "")[-6:] == "_Index"


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


def dataclass_init_exclude_keys(cls):
    """Method to return dataclass exclude init keys."""
    return getattr(cls, Constants.dataclass_decorator.INIT_EXCLUDE_KEYS, {})


def is_eval_env(cls):
    """Method to return flag that class is a eval env class."""
    return getattr(cls, Constants.dataclass_decorator.EVAL_ENV, False)


def is_chain_configs(cls):
    """Method to return flag that class is a chain files class."""
    return getattr(cls, Constants.config_decorator.chain_configs, False)


def dict_factory(cls):
    """Method to return class __dict_factory__."""
    return getattr(cls, Constants.dataclass_decorator.DICT_FACTORY, dict)


def value_factory(cls):
    """Method to return class __value_factory__."""
    return getattr(cls, Constants.dataclass_decorator.VALUE_FACTORY, None)


def alias_generator(cls):
    """Method to return class __alias_generator__."""
    return getattr(cls, Constants.config_decorator.ALIAS_GENERATOR, None)


def evaluate_default_configs(cls, config):
    """Method to evaluate default configs."""
    # if is_validated(cls):
    #     return config

    for key, field in dataclass_fields(cls).items():
        if isinstance(field.type, IndexInstance):
            config.pop(key, None)
    return config


def is_validated(cls):
    """Method to return flag that class is a validated class."""
    return getattr(cls, Constants.config_decorator.VALIDATE, False)


def normalized_class_name(cls):
    """Method to return class name normalized."""
    return re.sub(r"([a-z])([A-Z])", "\\1_\\2", getattr(cls, "__name__", "WrongConfigClass")).lower()


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
    return (
        cls.keys()
        if hasattr(cls, "keys")
        else [
            slot
            for slot in getattr(cls, Constants.dataclass_decorator.FIELDS, {}).keys()
            if slot not in getattr(cls, Constants.dataclass_decorator.IGNORED_SLOTS, [])
        ]
    )


def is_use_regex(cls):
    """Method to return flag that the config class can be empty."""
    return getattr(cls, Constants.config_decorator.USE_REGEX, False)


def is_allow_empty(cls):
    """Method to return flag that the config class can be empty."""
    return getattr(cls, Constants.config_decorator.ALLOW_EMPTY, False)


def pass_section_name(cls):
    """Method to return flag that the config has section_name in slots, so that the section title is passed in."""
    return Constants.config_decorator.SECTION_NAME_KEY in getattr(cls, Constants.dataclass_decorator.FIELDS, {})


def dc_field_without_default(field):
    """Checks if the dataclass has a default / default_factory."""
    return isinstance(field.default, WITHOUT_DEFAULT_TYPE) or isinstance(field.default_factory, WITHOUT_DEFAULT_TYPE)


def default(field):
    """Method to get the default value of the dataclass."""
    return (
        field.default_factory()
        if not isinstance(field.default_factory, (MISSING_TYPE, WITHOUT_DEFAULT_TYPE))
        else field.default
    )


def get_env_vars(dc_cls):
    """Method to get the environment variables for the dataclass."""
    return {key: eval_type(environ[key]) for key in dc_cls.__dataclass_fields__.keys() if key in environ.keys()}


def fields(class_or_instance):
    """Patched method of the dataclasses fields method to ignore the custom dataclass."""
    return dc_fields(class_or_instance)


dataclasses.fields = fields


def get_default_loader(files: Optional[List[str]] = None) -> Loader:
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


def get_loader_callback(loader):
    """Method to get the loader callback."""
    return yaml_load if loader == Loader.YAML else ini_load
