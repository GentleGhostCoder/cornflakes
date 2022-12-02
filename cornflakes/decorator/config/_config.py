import logging
from typing import Any, Callable, List, Optional, Union, cast

from cornflakes.decorator._types import Config, ConfigGroup, DataclassProtocol, Loader
from cornflakes.decorator.config._config_group import config_group
from cornflakes.decorator.config._helper import get_default_loader
from cornflakes.decorator.config.dict import create_dict_file_loader
from cornflakes.decorator.config.ini import create_ini_file_loader
from cornflakes.decorator.config.yaml import create_yaml_file_loader
from cornflakes.decorator.dataclass import dataclass


def config(
    config_cls=None,
    files: Optional[Union[List[str], str]] = None,
    sections: Optional[Union[List[str], str]] = None,
    use_regex: Optional[bool] = False,
    is_list: Optional[Union[bool, int]] = False,
    default_loader: Optional[Loader] = None,
    allow_empty: Optional[bool] = False,
    filter_function: Optional[Callable[..., bool]] = None,
    **kwargs,
) -> Union[Union[Config, ConfigGroup], Callable[..., Union[Config, ConfigGroup]]]:
    """Config decorator to parse Ini Files and implements config loader methods to config-classes.

    :param config_cls: Config class
    :param files: Default config files
    :param sections: Default config sections
    :param use_regex: Flag to eval all sections by regex
    :param is_list: Flag to load Config as List of this class
    :param default_loader: Default config parser method (enum)
    :param kwargs: Default configs to overwrite dataclass args
    :param allow_empty: Flag that allows empty config result
    :param filter_function: Optional filter method for config
    :param kwargs: Additional args for custom dataclass. (dict_factory, eval_env, validate. ...).

    :returns: wrapped class or the wrapper itself with the custom default arguments if the config class is not
    """
    sections = sections if isinstance(sections, list) else [sections] if sections else []
    files = files if isinstance(files, list) else [files] if files else []
    if not default_loader:
        default_loader = get_default_loader(files)

    def wrapper(cls):
        """Wrapper function for the config decorator config_decorator."""
        # Check __annotations__
        if not hasattr(cls, "__annotations__"):
            logging.warning(f"{cls.__name__} missing annotations for values!")
            return cls

        # Check is config
        if any([hasattr(slot, "__config_sections__") for slot in cls.__annotations__.values()]):
            logging.warning(
                "Wrapper config not working for a subset of config classes. "
                f"Please use {config_group.__name__} instead."
            )
            return config_group(
                config_cls=cls,
                files=files,
                **kwargs,
            )(cls)

        cls: Union[DataclassProtocol, Any] = dataclass(cls, **kwargs)
        cls.__config_sections__ = sections
        cls.__config_files__ = files
        cls.__multi_config__ = use_regex
        cls.__config_list__ = is_list
        cls.__allow_empty_config__ = allow_empty
        cls.__config_filter_function__ = filter_function
        cls.from_yaml = staticmethod(create_yaml_file_loader(cls=cls))
        cls.from_ini = staticmethod(create_ini_file_loader(cls=cls))  # class not dependent method
        cls.from_dict = staticmethod(create_dict_file_loader(cls=cls))
        cls.from_file = getattr(cls, str(default_loader.value), cls.from_dict)

        return cast(Config, cls)

    if config_cls:
        return wrapper(config_cls)  # type: ignore
    return wrapper
