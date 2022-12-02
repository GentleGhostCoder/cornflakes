# from collections import OrderedDict
import logging
from typing import Any, Callable, Dict, List, Optional, Union

from cornflakes.decorator._types import Config, ConfigGroup
from cornflakes.decorator.config._helper import is_config, is_config_list


def create_group_loader(cls) -> Callable[..., ConfigGroup]:
    """Config decorator to parse Ini Files and implements from_file method to config-group-classes.

    :param cls: Config class

    :returns: wrapped class or the wrapper itself with the custom default arguments if the config group class is not
    """

    def from_file(
        files: Optional[Union[Dict[str, Union[List[str], str]], List[str], str]] = None,
        sections: Optional[Union[List[str], str]] = None,
        config_dict: Optional[Dict[str, Any]] = None,
        filter_function: Optional[Callable[[Config], bool]] = None,
        eval_env: Optional[bool] = None,
        allow_empty: Optional[bool] = None,
        *slot_args,
        **slot_kwargs,
    ) -> ConfigGroup:
        """Config parser from config files.

        :param files: Default config files
        :param sections: Default config sections
        :param config_dict: Config dictionary to pass already loaded configs
        :param slot_kwargs: Default configs to overwrite passed class
        :param filter_function: Optional filter method for config
        :param eval_env: Flag to evaluate environment variables into default values.
        :param allow_empty: Flag that allows empty config result -> e.g. emtpy list
        :param slot_args: Default configs to overwrite passed class
        :param slot_kwargs: Default configs to overwrite passed class

        :returns: Nested Lists of Config Classes

        """
        if not files:
            files = cls.__config_files__

        # if not config_dict:
        #     config_dict = OrderedDict(loader({None: files}, eval_env=eval_env))
        #     print(config_dict)
        # logging.debug(f"Read config with sections: {config_dict.keys()}")
        for slot_class in list(getattr(cls, "__annotations__", {}).values())[len(slot_args) :]:
            if is_config_list(slot_class):
                slot_class = slot_class.__args__[0]
            if is_config(slot_class):
                slot_kwargs.update(
                    slot_class.from_file(
                        files=files,
                        sections=sections,
                        config_dict=config_dict,
                        filter_function=filter_function or cls.__config_filter_function__,
                        eval_env=eval_env,
                        allow_empty=allow_empty or cls.__allow_empty_config__,
                    )
                )
        error_args = [key for key in slot_kwargs if key not in cls.__dataclass_fields__]
        if error_args:
            logging.warning(f"The variables {error_args} in **{cls.__name__}** are not defined!")
            logging.warning("Use generate_group in build script to auto generate the config group!")

        return cls(*slot_args, **{key: value for key, value in slot_kwargs.items() if key not in error_args})

    return from_file  # class not dependent method
