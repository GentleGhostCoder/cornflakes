from collections import OrderedDict
import logging
import re
from typing import Any, Callable, Dict, List, Optional, Union

from cornflakes import ini_load
from cornflakes.decorator.config._helper import allow_empty, is_config_list, pass_section_name
from cornflakes.decorator.config._protocols import Config


def _none_omit(obj: list):
    return [v for v in obj if v is not None]


def create_file_loader(  # noqa: C901
    cls: Config,
    loader=ini_load,
) -> Callable[..., Dict[str, Union[Config, List[Config], None]]]:
    """Config decorator to parse Ini Files and implements from_file method to config-classes.

    :param cls: Config class
    :param loader: Config Loader (ini_load, yaml_load)

    :returns: wrapped class or the wrapper itself with the custom default arguments if the config class is not
    """

    def _create_config(config: dict, *cls_args, **cls_kwargs) -> Union[Config, None]:
        logging.debug(config)
        logging.debug(allow_empty(cls))
        if not config and allow_empty(cls):
            return
        config.update(cls_kwargs)
        error_args = [key for key in config if key not in getattr(cls, "__slots__", ())]
        if error_args:
            logging.warning(f"Some variables in **{cls.__name__}** have no annotation or are not defined!")
            logging.warning(f"Please check Args: {error_args}")
        #  config_instance
        config_instance = cls(
            *cls_args, **{key: value for key, value in config.items() if key in getattr(cls, "__slots__", ())}
        )
        return config_instance

    def from_file(
        files: Optional[Union[List[str], str]] = None,
        sections: Optional[Union[List[str], str]] = None,
        config_dict: Optional[Dict[str, Any]] = None,
        filter_function: Optional[Callable[[Config], bool]] = None,
        *slot_args,
        **slot_kwargs,
    ) -> Dict[str, Union[Config, List[Config], None]]:
        """Config parser from ini files.

        :param files: Default config files
        :param sections: Default config sections
        :param config_dict: Config dictionary to pass already loaded configs
        :param slot_args: Default configs to overwrite passed class
        :param slot_kwargs: Default configs to overwrite passed class
        :param filter_function: Optional filter method for config

        :returns: Nested Lists of Config Classes

        """
        if not sections:
            sections = cls.__config_sections__ or re.sub(r"([a-z])([A-Z])", "\\1_\\2", cls.__name__).lower()
        if not files:
            files = cls.__config_files__
        if not filter_function:
            filter_function = cls.__config_filter_function__ or (lambda x: True)

        pass_sections = pass_section_name(cls)

        def get_section_kwargs(section):
            return {**slot_kwargs, **({"section_name": section} if pass_sections else {})}

        if not cls.__multi_config__ and isinstance(sections, str):
            logging.debug(f"Load ini from file: {files} - section: {sections} for config {cls.__name__}")

            if not config_dict:
                config_dict = OrderedDict(
                    loader({None: files}, sections, getattr(cls, "__slots__", ())[len(slot_args) :])
                )
                logging.debug(f"Read config with sections: {config_dict.keys()}")
            config = _create_config(config_dict.get(sections, {}), *slot_args, **get_section_kwargs(sections))
            if not filter_function(config):
                return {sections: _create_config({}, *slot_args, **get_section_kwargs(sections))}
            return {sections: config}

        if not config_dict:
            config_dict = OrderedDict(loader({None: files}, None, getattr(cls, "__slots__", ())[len(slot_args) :]))
            logging.debug(f"Read config with sections: {config_dict.keys()}")

        regex = f'({"|".join(sections) if isinstance(sections, list) else sections})'
        logging.debug(f"Load all configs that mach **{regex}**")

        config_dict = {section: config for section, config in config_dict.items() if bool(re.match(regex, section))}

        if not is_config_list(cls):
            return {
                section: config
                for section, config in {
                    section: _create_config(config_dict.get(section, {}), *slot_args, **slot_kwargs)
                    for section in config_dict
                }.items()
                if filter_function(config)
            } or {
                re.sub(r"([a-z])([A-Z])", "\\1_\\2", cls.__name__).lower(): _create_config(
                    {}, *slot_args, **slot_kwargs  # no matches
                )
            }

        return {
            re.sub(r"([a-z])([A-Z])", "\\1_\\2", cls.__name__).lower(): (
                list(
                    filter(
                        filter_function,
                        _none_omit(
                            [
                                _create_config(config_dict.get(section, {}), *slot_args, **get_section_kwargs(section))
                                for section in config_dict
                            ]
                        ),
                    )
                )
                or _none_omit([_create_config({}, *slot_args, **slot_kwargs)] * is_config_list(cls))
            )
        }

    return from_file
