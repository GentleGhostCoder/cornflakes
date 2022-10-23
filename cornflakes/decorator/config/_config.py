from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Union

from cornflakes import ini_load
from cornflakes.decorator._add_dataclass_slots import add_slots
from cornflakes.decorator.config._config_group import config_group
from cornflakes.decorator.config._dict import create_dict_file_loader, to_dict
from cornflakes.decorator.config._ini import create_ini_file_loader, to_ini, to_ini_bytes
from cornflakes.decorator.config._loader import (
    DICT_LOADER,
    DICT_PARSER,
    INI_BYTES_PARSER,
    INI_LOADER,
    INI_WRITER,
    YAML_BYTES_PARSER,
    YAML_LOADER,
    YAML_WRITER,
)
from cornflakes.decorator.config._yaml import create_yaml_file_loader, to_yaml, to_yaml_bytes
from cornflakes.logging import logger


def config(  # noqa: C901
    config_cls=None,
    files: Union[str, List[str]] = None,
    sections: Union[str, List[str]] = None,
    use_regex: bool = False,
    is_list: Union[bool, int] = False,
    *args,
    loader: Callable[
        [
            Union[
                Union[str, List[str], Dict[Union[str, None], Union[str, List[str]]]],
                Optional[Union[str, List[str], Dict[Union[str, None], Union[str, List[str]]]]],
                Optional[Union[str, List[str], Dict[Union[str, None], Union[str, List[str]]]]],
                Optional[Union[str, List[str], Dict[str, Any]]],
            ]
        ],
        Dict,
    ] = ini_load,
    **kwargs,
):
    """Config decorator to parse Ini Files and implements config loader methods to config-classes.

    :param config_cls: Config class
    :param files: Default config files
    :param sections: Default config sections
    :param use_regex: Flag to eval all sections by regex
    :param is_list: Flag to load Config as List of this class
    :param loader: Config Loader (ini_load, yaml_load)
    :param args: Default configs to overwrite dataclass args
    :param kwargs: Default configs to overwrite dataclass args

    :returns: wrapped class or the wrapper itself with the custom default arguments if the config class is not
    """

    def wrapper(cls):
        """Wrapper function for the config decorator config_decorator."""
        # Check __annotations__
        if not hasattr(cls, "__annotations__"):
            logger.warning(f"{cls.__name__} missing annotations for values!")
            return cls

        # Check is config
        if any([hasattr(slot, "__config_sections__") for slot in cls.__annotations__.values()]):
            logger.warning(
                "Wrapper config not working for a subset of config classes. "
                f"Please use {config_group.__name__} instead."
            )
            return config_group(
                *args,
                config_cls=cls,
                files=files,
                loader=loader,
                **kwargs,
            )

        cls = add_slots(dataclass(cls, *args, **kwargs))
        cls.__config_sections__ = sections
        cls.__config_files__ = files
        cls.__multi_config__ = use_regex
        cls.__config_list__ = is_list

        def _new(self, *new_args, **new_kwargs):
            # two chars missing in original of next line ...
            setattr(self, DICT_PARSER, to_dict)
            setattr(self, INI_WRITER, to_ini)
            setattr(self, YAML_WRITER, to_yaml)
            setattr(self, YAML_BYTES_PARSER, to_yaml_bytes)
            setattr(self, INI_BYTES_PARSER, to_ini_bytes)
            return super(cls, self).__new__(self)

        cls.__new__ = classmethod(_new)

        setattr(cls, YAML_LOADER, staticmethod(create_yaml_file_loader(cls=cls)))
        setattr(cls, INI_LOADER, staticmethod(create_ini_file_loader(cls=cls)))
        setattr(cls, DICT_LOADER, staticmethod(create_dict_file_loader(cls=cls)))

        return cls

    if config_cls:
        return wrapper(config_cls)
    return wrapper
