from collections import OrderedDict
from functools import partial
import logging
import re
from typing import Any, Callable, Dict, List, Optional, Union

from cornflakes import ini_load
from cornflakes.common import recursive_update
from cornflakes.decorator.dataclasses._helper import (
    alias_generator,
    dataclass_fields,
    dataclass_required_keys,
    is_chain_configs,
    is_config,
    is_config_list,
    is_use_regex,
    normalized_class_name,
    pass_section_name,
)
from cornflakes.types import Constants

logger = logging.getLogger(__name__)


def create_file_loader(  # noqa: C901
    cls,
    _loader_callback=ini_load,  # type: ignore
    _instantiate: bool = True,
):
    """Config decorator to parse Ini Files and implements from_file method to config-classes.

    :param _instantiate: If True, the config class will be initialized with the parsed config dict.
    :param cls: Config class
    :param _loader_callback: Config Loader (ini_load, yaml_load)

    :returns: wrapped class or the wrapper itself with the custom default arguments if the config class is not
    """
    if not is_config(cls):
        raise TypeError(f"Class {cls.__name__} is not a config class!")

    required_keys = dataclass_required_keys(
        cls
    )  # [key for key, f in dataclass_fields(cls).items() if dc_slot_missing_default(f)]  # type: ignore
    _alias_generator: Optional[Callable[[str], str]] = alias_generator(cls)
    if _alias_generator and callable(_alias_generator):
        keys = {
            key: [getattr(f, "aliases", key), _alias_generator(key)] or key for key, f in dataclass_fields(cls).items()
        }
    else:
        keys = {key: getattr(f, "aliases", key) or key for key, f in dataclass_fields(cls).items()}

    def _create_config(config_args: dict, allow_empty=None, **cls_kwargs) -> Optional[Union[dict, Any]]:
        if not config_args and allow_empty:
            return None
        config_args.update(cls_kwargs)
        error_args = [key for key in config_args if key not in [*dataclass_fields(cls)]]
        if error_args:
            logger.debug(f"Some variables in **{cls.__name__}** have no annotation or are not defined!")
            logger.debug(f"Please check Args: {error_args}")

        #  config_instance
        if _instantiate:
            return cls(
                **{key: value for key, value in config_args.items() if key in dataclass_fields(cls)},
                init_from_default_cache=True,
            )
        return {key: value for key, value in config_args.items() if key in dataclass_fields(cls)}

    def _check_required_fields(config_args) -> dict:
        return {
            section: config
            for section, config in config_args.items()
            if not any(True for key in required_keys if key not in config.keys())
        }

    def _check_any_key_in_fields(config_args) -> dict:
        return {
            section: config
            for section, config in config_args.items()
            if any(key in dataclass_fields(cls).keys() for key in config.keys())
        }

    def _check_config_dict(config_args) -> dict:
        config_args = _check_required_fields(config_args)
        config_args = _check_any_key_in_fields(config_args)
        config_args = _rename_default_section(config_args)
        return config_args or {}

    def _rename_default_section(config_args) -> dict:
        if None not in config_args:
            return config_args
        config_args["default"] = config_args.pop(None)
        return config_args or {}

    def from_file(
        files: Optional[List[str]] = None,
        sections: Optional[List[str]] = None,
        config_dict: Optional[Dict[str, Any]] = None,
        eval_env: Optional[bool] = None,
        allow_empty: Optional[bool] = None,
        **slot_kwargs,
    ):
        """Config parser from ini files.

        :param files: Default config files
        :param sections: Default config sections
        :param config_dict: Config dictionary to pass already loaded configs
        :param slot_kwargs: Default configs to overwrite passed class
        :param eval_env: Flag to evaluate environment variables into default values.
        :param allow_empty: Flag that allows empty config result -> e.g. emtpy list

        :returns: Nested Lists of Config Classes
        """
        if not sections:
            sections = getattr(cls, Constants.config_decorator.SECTIONS, None)
        if not files:
            files = getattr(cls, Constants.config_decorator.FILES, None)
        if not eval_env:
            eval_env = getattr(cls, Constants.dataclass_decorator.EVAL_ENV, None)
        if not allow_empty:
            allow_empty = getattr(cls, Constants.config_decorator.ALLOW_EMPTY, None)

        create_config = partial(_create_config, allow_empty=allow_empty)
        normalized_cls_name = normalized_class_name(cls)
        chain_configs = is_chain_configs(cls)
        pass_sections = pass_section_name(cls)

        def get_section_kwargs(value: str):
            """Get section kwargs.

            :param value: Section name
            """
            return {**slot_kwargs, **({Constants.config_decorator.SECTION_NAME_KEY: value} if pass_sections else {})}

        if not is_use_regex(cls) and not is_config_list(cls) and sections and len(sections) == 1:
            section = sections[0]
            logger.debug(f"Load ini from file: {files} - section: {section} for config {cls.__name__}")

            if not config_dict:
                config_dict = OrderedDict(
                    _loader_callback(files={None: files}, sections=section, keys=keys, defaults=None, eval_env=eval_env)
                )
                config_dict = _check_config_dict(config_dict)

            if not section and config_dict.keys():
                section = config_dict.popitem()[0] or normalized_cls_name

            config = create_config(config_dict.get(section, {}), **get_section_kwargs(section))

            if chain_configs:
                section = normalized_cls_name

            if not config:
                return {section: create_config({}, **get_section_kwargs(section))}
            return {section: config}

        if not config_dict:
            raw_config_dict = OrderedDict(_loader_callback(files=files, sections=None, keys=keys, eval_env=eval_env))
            config_dict = {}
            for file_name, section_config in raw_config_dict.items():
                for section_name, config in section_config.items():
                    config_dict[f"{file_name}:{section_name or normalized_cls_name}"] = config
            config_dict = _check_config_dict(config_dict)

            logger.debug(f"Read config with sections: {config_dict.keys()}")

        regex = f'({"|".join(sections) if isinstance(sections, list) else sections or ""})'
        logger.debug(f"Load all configs that match regex: `{regex}`")
        sections_found = [
            section for section in config_dict if bool(re.match(regex, section.split(":", 1).pop() or ""))
        ]
        if chain_configs:
            new_config: Dict[str, Any] = {normalized_cls_name: {}}
            if not sections_found:
                sections_found = list(config_dict.keys())
            for section in sections_found:
                recursive_update(new_config[normalized_cls_name], config_dict.pop(section), merge_lists=True)
            config_dict = new_config
        else:
            config_dict = {section: config for section, config in config_dict.items() if section in sections_found}

        if not is_config_list(cls):
            return {
                section.split(":", 1).pop(): config
                for section, config in {
                    section: create_config(
                        config_dict.get(section, {}), **get_section_kwargs(section.split(":", 1).pop())
                    )
                    for section in config_dict
                }.items()
                if config
            } or {
                normalized_cls_name: create_config({}, **slot_kwargs)  # no matches
            }

        return {
            normalized_cls_name: (
                list(
                    _none_omit(
                        [
                            create_config(
                                config_dict.get(section, {}), **get_section_kwargs(section.split(":", 1).pop())
                            )
                            for section in config_dict
                        ]
                    ),
                )
                or _none_omit([create_config({}, **slot_kwargs)] * is_config_list(cls))
            )
        }

    return from_file


def _none_omit(obj: list):
    return [v for v in obj if v is not None]


def _default_filter_method(x: Any):
    return True
