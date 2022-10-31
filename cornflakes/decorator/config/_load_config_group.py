from collections import OrderedDict
import logging
from typing import Any, Callable, Dict, List, Union

from cornflakes import ini_load
from cornflakes.decorator.config._helper import is_config, is_config_list
from cornflakes.decorator.config._protocols import Config, ConfigGroup, ConfigGroupLoader


def create_group_loader(
    cls=None,
    loader: ConfigGroupLoader = ini_load,
) -> Callable[..., ConfigGroup]:
    """Config decorator to parse Ini Files and implements from_file method to config-group-classes.

    :param cls: Config class
    :param loader: Config Loader (ini_load, yaml_load)

    :returns: wrapped class or the wrapper itself with the custom default arguments if the config group class is not
    """

    def from_file(
        files: Union[str, List[str], Dict[str, Union[str, List[str]]]] = None,
        config_dict: Dict[str, Any] = None,
        filter_function: Callable[[Config], bool] = None,
        *slot_args,
        **slot_kwargs,
    ) -> ConfigGroup:
        """Config parser from config files.

        :param files: Default config files
        :param config_dict: Config dictionary to pass already loaded configs
        :param slot_args: Default configs to overwrite passed class
        :param slot_kwargs: Default configs to overwrite passed class
        :param filter_function: Optional filter method for config

        :returns: Nested Lists of Config Classes

        """
        if not files:
            files = cls.__config_files__

        if not config_dict:
            config_dict = OrderedDict(loader({None: files}))
        logging.debug(f"Read config with sections: {config_dict.keys()}")
        for slot_name, slot_class in list(cls.__annotations__.items())[len(slot_args) :]:
            if is_config_list(slot_class):
                slot_class = slot_class.__args__[0]
            if is_config(slot_class):
                slot_kwargs.update(
                    slot_class.from_dict(config_dict=config_dict, sections=slot_name, filter_function=filter_function)
                )
        error_args = [key for key in slot_kwargs if key not in cls.__slots__]
        if error_args:
            logging.warning(f"The variables {error_args} in **{cls.__name__}** are not defined!")
            logging.warning("Use generate_group in build script to auto generate the config group!")

        return cls(*slot_args, **{key: value for key, value in slot_kwargs.items() if key not in error_args})

    return from_file  # class not dependent method
