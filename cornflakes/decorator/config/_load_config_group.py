from typing import Any, Callable, Dict, List, Union

from cornflakes import ini_load
from cornflakes.decorator.config._loader import DICT_LOADER
from cornflakes.logging import logger


def create_group_loader(
    cls=None,
    loader: Callable[
        [
            Dict[Union[str, None], Union[str, List[str]]],
        ],
        Dict,
    ] = ini_load,
):
    """Config decorator to parse Ini Files and implements from_file method to config-group-classes.

    :param cls: Config class
    :param loader: Config Loader (ini_load, yaml_load)

    :returns: wrapped class or the wrapper itself with the custom default arguments if the config group class is not
    """

    def from_file(
        files: Union[str, List[str], Dict[str, Union[str, List[str]]]] = None,
        config_dict: Dict[str, Any] = None,
        *slot_args,
        **slot_kwargs,
    ) -> cls:
        """Config parser from config files.

        :param files: Default config files
        :param config_dict: Config dictionary to pass already loaded configs
        :param slot_args: Default configs to overwrite passed class
        :param slot_kwargs: Default configs to overwrite passed class

        :returns: Nested Lists of Config Classes

        """
        if not files:
            files = cls.__config_files__

        if not config_dict:
            config_dict = loader({None: files})
        logger.debug(f"Read config with sections: {config_dict.keys()}")
        for slot_class in list(cls.__annotations__.values())[len(slot_args) :]:
            is_list = hasattr(slot_class, "__args__")
            if is_list:
                slot_class = slot_class.__args__[0]
            if hasattr(slot_class, "__config_sections__"):
                slot_kwargs.update(getattr(slot_class, DICT_LOADER)(config_dict=config_dict))
        error_args = [key for key in slot_kwargs if key not in cls.__slots__]
        if error_args:
            logger.warning(f"The variables {error_args} in **{cls.__name__}** are not defined!")
            logger.warning("Use generate_group in build script to auto generate the config group!")

        return cls(*slot_args, **{key: value for key, value in slot_kwargs.items() if key not in error_args})

    return from_file  # class not dependent method
