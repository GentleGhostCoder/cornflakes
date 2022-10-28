import logging
import re
from typing import Any, Callable, Dict, List, Union

from cornflakes import ini_load
from cornflakes.decorator.config._protocols import Config, ConfigLoader


def create_file_loader(
    cls=None,
    loader: ConfigLoader = ini_load,
) -> Callable[..., Dict[str, Union[Config, List[Config]]]]:
    """Config decorator to parse Ini Files and implements from_file method to config-classes.

    :param cls: Config class
    :param loader: Config Loader (ini_load, yaml_load)

    :returns: wrapped class or the wrapper itself with the custom default arguments if the config class is not
    """

    def _create_config(config: dict, *cls_args, **cls_kwargs):
        config.update(cls_kwargs)
        error_args = [key for key in config if key not in cls.__slots__]
        if error_args:
            logging.warning(f"Some variables in **{cls.__name__}** have no annotation or are not defined!")
            logging.warning(f"Please check Args: {error_args}")
        #  config_instance
        config_instance = cls(*cls_args, **{key: value for key, value in config.items() if key in cls.__slots__})
        return config_instance

    def from_file(
        files: Union[str, List[str]] = None,
        sections: Union[str, List[str]] = None,
        config_dict: Dict[str, Any] = None,
        *slot_args,
        **slot_kwargs,
    ) -> Dict[str, Union[Config, List[Config]]]:
        """Config parser from ini files.

        :param files: Default config files
        :param sections: Default config sections
        :param config_dict: Config dictionary to pass already loaded configs
        :param slot_args: Default configs to overwrite passed class
        :param slot_kwargs: Default configs to overwrite passed class

        :returns: Nested Lists of Config Classes

        """
        if not sections:
            sections = cls.__config_sections__ or re.sub(r"([a-z])([A-Z])", "\\1_\\2", cls.__name__).lower()
        if not files:
            files = cls.__config_files__
        if not cls.__multi_config__ and isinstance(sections, str):
            logging.debug(f"Load ini from file: {files} - section: {sections} for config {cls.__name__}")
            if not config_dict:
                config_dict = loader({None: files}, sections, cls.__slots__[len(slot_args) :])
                logging.debug(f"Read config with sections: {config_dict.keys()}")
            return {sections: _create_config(config_dict.get(sections, {}), *slot_args, **slot_kwargs)}

        if not config_dict:
            config_dict = loader({None: files}, None, cls.__slots__[len(slot_args) :])
            logging.debug(f"Read config with sections: {config_dict.keys()}")
        regex = f'({"|".join(sections) if isinstance(sections, list) else sections})'
        logging.debug(f"Load all configs that mach **{regex}**")
        if not cls.__config_list__:
            return {
                section: _create_config(config_dict, *slot_args, **slot_kwargs)
                for section, config_dict in (
                    config_dict.items()
                    or isinstance(sections, str)
                    and [(sections, {})]
                    or [(section, {}) for section in sections]
                )
                if bool(re.match(regex, section))
            } or {
                re.sub(r"([a-z])([A-Z])", "\\1_\\2", cls.__name__).lower(): _create_config(
                    config_dict, *slot_args, **slot_kwargs
                )
            }
        return {
            re.sub(r"([a-z])([A-Z])", "\\1_\\2", cls.__name__).lower(): [
                _create_config(config_dict, *slot_args, **slot_kwargs)
                for section, config_dict in (
                    config_dict.items()
                    or isinstance(sections, str)
                    and [(sections, {})]
                    or [(section, {}) for section in sections]
                )
                if bool(re.match(regex, section))
            ]
            or [_create_config(config_dict, *slot_args, **slot_kwargs)] * cls.__config_list__
        }

    return from_file
