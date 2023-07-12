import logging
from typing import Callable, List, Optional, Union

from cornflakes.decorator import Index, funcat
from cornflakes.decorator.config._config_group import config_group
from cornflakes.decorator.config.dict import create_dict_file_loader
from cornflakes.decorator.config.ini import create_ini_file_loader
from cornflakes.decorator.config.yaml import create_yaml_file_loader
from cornflakes.decorator.dataclass import dataclass
from cornflakes.decorator.dataclass.helper import get_default_loader
from cornflakes.decorator.types import Config, ConfigGroup, Constants, Dataclass, Loader


def config(
    config_cls=None,
    files: Optional[Union[List[str], str]] = None,
    sections: Optional[Union[List[str], str]] = None,
    use_regex: Optional[bool] = False,
    is_list: Optional[Union[bool, int]] = False,
    default_loader: Optional[Loader] = None,
    allow_empty: Optional[bool] = False,
    chain_files: Optional[bool] = False,
    filter_function: Optional[Callable[..., bool]] = None,
    **kwargs,
) -> Union[Union[Dataclass, Config, ConfigGroup], Callable[..., Union[Dataclass, Config, ConfigGroup]]]:
    """Config decorator to parse Ini Files and implements config loader methods to config-classes.

    :param config_cls: Config class
    :param files: Default config files
    :param sections: Default config sections
    :param use_regex: Flag to eval all sections by regex
    :param is_list: Flag to load Config as List of this class
    :param default_loader: Default config parser method (enum)
    :param kwargs: Default configs to overwrite dataclass args
    :param allow_empty: Flag that allows empty config result
    :param chain_files: flag indicating whether to chain files in to single config.
    :param filter_function: Optional filter method for config
    :param kwargs: Additional args for custom dataclass. (dict_factory, eval_env, validate. ...).

    :returns: wrapped class or the wrapper itself with the custom default arguments if the config class is not
    """
    sections = sections if isinstance(sections, list) else [sections] if sections else []
    files = files if isinstance(files, list) else [files] if files else []
    if not default_loader:
        default_loader = get_default_loader(files)

    def wrapper(cls) -> Union[Dataclass, Config, ConfigGroup]:
        """Wrapper function for the config decorator config_decorator."""
        # Check __annotations__
        if not hasattr(cls, "__annotations__"):
            logging.warning(f"{cls.__name__} missing annotations for values!")
            return cls

        # Check is config
        if any(hasattr(slot, Constants.config_decorator.SECTIONS) for slot in cls.__annotations__.values()):
            logging.warning(
                "Wrapper config not working for a subset of config classes. "
                f"Please use {config_group.__name__} instead."
            )
            return config_group(
                config_cls=cls,
                files=files,
                **kwargs,
            )(cls)

        cls = dataclass(cls, **kwargs)

        setattr(cls, Constants.config_decorator.SECTIONS, sections)
        setattr(cls, Constants.config_decorator.FILES, files)
        setattr(cls, Constants.config_decorator.USE_REGEX, use_regex)
        setattr(cls, Constants.config_decorator.IS_LIST, is_list)
        setattr(cls, Constants.config_decorator.CHAIN_FILES, chain_files)
        setattr(cls, Constants.config_decorator.ALLOW_EMPTY, allow_empty)
        setattr(cls, Constants.config_decorator.FILTER_FUNCTION, filter_function)

        setattr(
            cls,
            Loader.YAML.value,
            staticmethod(funcat(Index.reset, funcat_where="wrap")(create_yaml_file_loader(cls=cls))),
        )
        setattr(
            cls,
            Loader.INI.value,
            staticmethod(funcat(Index.reset, funcat_where="wrap")(create_ini_file_loader(cls=cls))),
        )
        setattr(
            cls,
            Loader.DICT.value,
            staticmethod(funcat(Index.reset, funcat_where="wrap")(create_dict_file_loader(cls=cls))),
        )
        setattr(
            cls,
            Loader.FILE.value,
            funcat(Index.reset, funcat_where="wrap")(
                getattr(cls, str(default_loader.value), getattr(cls, Loader.DICT.value))
            ),
        )

        return cls

    return wrapper(config_cls) if config_cls else wrapper
