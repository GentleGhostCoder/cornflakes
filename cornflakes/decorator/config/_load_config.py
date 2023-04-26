from collections import OrderedDict
from dataclasses import MISSING
from functools import partial
import logging
import re
from typing import Any, Callable, Dict, List, Optional, Union

from cornflakes import ini_load
from cornflakes.decorator.dataclass.helper import (
    dataclass_fields,
    is_config_list,
    is_multi_config,
    normalized_class_name,
    pass_section_name,
)
from cornflakes.decorator.types import WITHOUT_DEFAULT, Config, LoaderMethod


def _none_omit(obj: list):
    return [v for v in obj if v is not None]


def _default_filter_method(x: Any):
    return True


def create_file_loader(  # noqa: C901
    cls: Union[Config, Any],
    loader: LoaderMethod = ini_load,  # type: ignore
):
    """Config decorator to parse Ini Files and implements from_file method to config-classes.

    :param cls: Config class
    :param loader: Config Loader (ini_load, yaml_load)

    :returns: wrapped class or the wrapper itself with the custom default arguments if the config class is not
    """
    required_keys = [
        key
        for key, f in dataclass_fields(cls).items()
        if (f.default_factory == WITHOUT_DEFAULT) or (f.default_factory == MISSING and f.default == MISSING)
    ]  # type: ignore

    keys = {key: getattr(f, "alias", key) or key for key, f in dataclass_fields(cls).items()}

    def create_config(config: dict, allow_empty=None, filter_function=None, **cls_kwargs):
        if not filter_function:
            filter_function = _default_filter_method
        if not config and allow_empty:
            return
        config.update(cls_kwargs)
        error_args = [key for key in config if key not in dataclass_fields(cls)]
        if error_args:
            logging.debug(f"Some variables in **{cls.__name__}** have no annotation or are not defined!")
            logging.debug(f"Please check Args: {error_args}")

        #  config_instance
        config_instance = cls(**{key: value for key, value in config.items() if key in dataclass_fields(cls)})
        if filter_function(config_instance):
            return config_instance

    def _check_required_fields(config_dict):
        return {
            section: config
            for section, config in config_dict.items()
            if not any([True for key in required_keys if key not in config.keys()])
        }

    def _check_any_key_in_fields(config_dict):
        return {
            section: config
            for section, config in config_dict.items()
            if any([key in dataclass_fields(cls).keys() for key in config.keys()])
        }

    def _check_config_dict(config_dict):
        config_dict = _check_required_fields(config_dict)
        config_dict = _check_any_key_in_fields(config_dict)
        config_dict = _rename_default_section(config_dict)
        return config_dict

    def _rename_default_section(config_dict):
        if None not in config_dict:
            return config_dict
        config_dict["default"] = config_dict.pop(None)
        return config_dict

    def from_file(
        files: Optional[Union[List[str], str]] = None,
        sections: Optional[Union[List[str], str]] = None,
        config_dict: Optional[Dict[str, Any]] = None,
        filter_function: Optional[Callable[[Config], bool]] = None,
        eval_env: Optional[bool] = None,
        allow_empty: Optional[bool] = None,
        **slot_kwargs,
    ) -> Union[Config, Any]:
        """Config parser from ini files.

        :param files: Default config files
        :param sections: Default config sections
        :param config_dict: Config dictionary to pass already loaded configs
        :param slot_kwargs: Default configs to overwrite passed class
        :param filter_function: Optional filter method for config
        :param eval_env: Flag to evaluate environment variables into default values.
        :param allow_empty: Flag that allows empty config result -> e.g. emtpy list

        :returns: Nested Lists of Config Classes
        """
        if not sections:
            sections = cls.__config_sections__
        if not files:
            files = cls.__config_files__
        if not filter_function:
            filter_function = cls.__config_filter_function__ or _default_filter_method
        if not eval_env:
            eval_env = cls.__eval_env__
        if not allow_empty:
            allow_empty = cls.__allow_empty_config__

        _create_config = partial(create_config, allow_empty=allow_empty, filter_function=filter_function)

        pass_sections = pass_section_name(cls)

        def get_section_kwargs(section):
            return {**slot_kwargs, **({"section_name": section} if pass_sections else {})}

        if not is_multi_config(cls) and isinstance(sections, str):
            logging.debug(f"Load ini from file: {files} - section: {sections} for config {cls.__name__}")

            if not config_dict:
                config_dict = OrderedDict(
                    loader(files={None: files}, sections=sections, keys=keys, defaults=None, eval_env=eval_env)
                )
                config_dict = _check_config_dict(config_dict)
                logging.debug(f"Read config with sections: {config_dict.keys()}")

            if not sections and config_dict.keys():
                sections = config_dict.popitem()[0] or normalized_class_name(cls)

            config = _create_config(config_dict.get(sections, {}), **get_section_kwargs(sections))
            if not config:
                return {sections: _create_config({}, **get_section_kwargs(sections))}
            return {sections: config}

        if not config_dict:
            if cls.__chain_files__:
                config_dict = OrderedDict(loader(files={None: files}, sections=None, keys=keys, eval_env=eval_env))
            else:
                raw_config_dict = OrderedDict(loader(files=files, sections=None, keys=keys, eval_env=eval_env))
                config_dict = {}
                for file_name, section_config in raw_config_dict.items():
                    for section_name, config in section_config.items():
                        config_dict[f"{file_name}:{section_name or normalized_class_name(cls)}"] = config
                config_dict = _check_config_dict(config_dict)

            logging.debug(f"Read config with sections: {config_dict.keys()}")

        regex = f'({"|".join(sections) if isinstance(sections, list) else sections or ""})'
        logging.debug(f"Load all configs that mach **{regex}**")

        config_dict = {
            section: config
            for section, config in config_dict.items()
            if bool(re.match(regex, section.split(":", 1).pop() or ""))
        }
        if not is_config_list(cls):
            return {
                section.split(":", 1).pop(): config
                for section, config in {
                    section: _create_config(
                        config_dict.get(section, {}), **get_section_kwargs(section.split(":", 1).pop())
                    )
                    for section in config_dict
                }.items()
                if config
            } or {
                normalized_class_name(cls): _create_config({}, **slot_kwargs)  # no matches
            }

        return {
            normalized_class_name(cls): (
                list(
                    _none_omit(
                        [
                            _create_config(
                                config_dict.get(section, {}), **get_section_kwargs(section.split(":", 1).pop())
                            )
                            for section in config_dict
                        ]
                    ),
                )
                or _none_omit([_create_config({}, **slot_kwargs)] * is_config_list(cls))
            )
        }

    return from_file
