import logging
from typing import Callable, List, Optional, Type, Union, cast

from cornflakes.decorator._add_dataclass_slots import add_slots
from cornflakes.decorator.config._config_group import config_group
from cornflakes.decorator.config._dataclass import dataclass
from cornflakes.decorator.config._dict import create_dict_file_loader, to_dict
from cornflakes.decorator.config._ini import create_ini_file_loader, to_ini, to_ini_bytes
from cornflakes.decorator.config._loader import Loader
from cornflakes.decorator.config._protocols import Config, ConfigGroup
from cornflakes.decorator.config._yaml import create_yaml_file_loader, to_yaml, to_yaml_bytes


def config(  # noqa: C901
    config_cls=None,
    files: Optional[Union[List[str], str]] = None,
    sections: Optional[Union[List[str], str]] = None,
    use_regex: Optional[bool] = False,
    is_list: Optional[Union[bool, int]] = False,
    default_loader: Loader = Loader.INI_LOADER,
    allow_empty: Optional[bool] = False,
    filter_function: Optional[Callable[..., bool]] = None,
    eval_env: bool = False,
    *args,
    **kwargs,
) -> Union[Union[Config, ConfigGroup], Callable[..., Union[Config, ConfigGroup]]]:
    """Config decorator to parse Ini Files and implements config loader methods to config-classes.

    :param config_cls: Config class
    :param files: Default config files
    :param sections: Default config sections
    :param use_regex: Flag to eval all sections by regex
    :param is_list: Flag to load Config as List of this class
    :param default_loader: Default config parser method (enum)
    :param args: Default configs to overwrite dataclass args
    :param kwargs: Default configs to overwrite dataclass args
    :param allow_empty: Flag that allows empty config result
    :param filter_function: Optional filter method for config
    :param eval_env: Flag to evaluate environment variables into default values.

    :returns: wrapped class or the wrapper itself with the custom default arguments if the config class is not
    """

    def wrapper(cls) -> Union[Config, ConfigGroup]:
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
                *args,
                config_cls=cls,
                files=files,
                **kwargs,
            )(cls)

        cls = add_slots(dataclass(cls, *args, **kwargs))
        cls.__config_sections__ = sections if isinstance(sections, list) else [sections] if sections else []
        cls.__config_files__ = files if isinstance(files, list) else [files] if files else []
        cls.__multi_config__ = use_regex
        cls.__config_list__ = is_list
        cls.__ignored_slots__ = [
            key for key in getattr(cls, "__slots__", ()) if getattr(cls.__dataclass_fields__[key], "ignore", False)
        ]
        cls.__allow_empty_config__ = allow_empty
        cls.__config_filter_function__ = filter_function
        cls.__eval_env__ = eval_env

        def new(self, *new_args, **new_kwargs):
            # two chars missing in original of next line ...
            self.to_dict = to_dict
            self.to_ini = to_ini
            self.to_yaml = to_yaml
            self.to_yaml_bytes = to_yaml_bytes
            self.to_ini_bytes = to_ini_bytes
            return super(cls, self).__new__(self)

        cls.__new__ = classmethod(new)

        cls.from_yaml = staticmethod(create_yaml_file_loader(cls=cls))
        cls.from_ini = staticmethod(create_ini_file_loader(cls=cls))  # class not dependent method
        cls.from_dict = staticmethod(create_dict_file_loader(cls=cls))
        cls.from_file = getattr(cls, str(default_loader.value), cls.from_ini)

        return cast(Type[Config], cls)

    if config_cls:
        return wrapper(config_cls)
    return wrapper
