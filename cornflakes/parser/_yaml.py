from os import environ
from os.path import abspath, expanduser
from typing import Any, Dict, List, Optional, Type, Union, cast

import yaml
from yaml import SafeLoader, UnsafeLoader

from cornflakes.common import recursive_update


def _get_updated_key(config: Dict, values: List[str], defaults: Dict):
    result = None
    for value in values:
        if key := config.get(value, defaults.get(value)):
            result = key
    return result


def _get_values(config, value: Union[str, List[str]], defaults: Dict):
    return (
        config
        if isinstance(config, str)
        else _get_updated_key(config, value, defaults)
        if isinstance(value, list)
        else config.get(value, defaults.get(value))
    )


def _get_section(
    config: dict,
    keys: dict,
    defaults: dict,
) -> dict:
    return {sub_key: _get_values(config, sub_value, defaults) for sub_key, sub_value in keys.items()}


def _get_all_sections(
    config: dict,
    sections: dict,
    keys: dict,
    defaults: dict,
) -> dict:
    new_config: dict = {}
    for section_key, section_names in sections.items():
        if not section_key:
            if isinstance(section_names, str):
                recursive_update(new_config, _get_section(config.get(section_names, {}), keys, defaults))
                continue
            for section in section_names:
                recursive_update(new_config, _get_section(config.get(section, {}), keys, defaults))
        if isinstance(section_names, str):
            recursive_update(new_config, {section_key: _get_section(config.get(section_names, {}), keys, defaults)})
            continue
        for section in section_names:
            recursive_update(new_config, {section_key: _get_section(config.get(section, {}), keys, defaults)})
    return new_config


def _yaml_read(
    file: str,
    sections: dict,
    keys: dict,
    defaults: dict,
    loader: Optional[Union[Type[UnsafeLoader], Type[SafeLoader]]],
) -> dict:
    with open(abspath(expanduser(file)), "rb") as f:
        data = f.read()
        if not loader:
            loader = yaml.UnsafeLoader if b": !!" in data else yaml.SafeLoader
        config = yaml.load(data, Loader=loader)  # noqa: S506
        if not sections:
            if not keys:
                return config
            return _get_all_sections(config, _to_map(list(config.keys())), keys, defaults)
        return _get_all_sections(config, sections, keys, defaults)


def _to_map(obj: Optional[Union[dict, list, tuple, str]]) -> dict:
    return (
        isinstance(obj, str)
        and {obj: obj}  # string
        or (isinstance(obj, list) or isinstance(obj, tuple))
        and {key: key for key in obj}  # list
        or cast(dict, obj)
        or {}
    )  # dict


def yaml_load(
    files: Union[str, List[str], Dict[str, Union[str, List[str]]]],
    sections: Optional[Union[str, List[str], Dict[Optional[str], Union[str, List[str]]]]] = None,
    keys: Optional[Union[str, List[str], Dict[str, Union[str, List[str]]]]] = None,
    defaults: Optional[Union[str, List[str], Dict[str, Any]]] = None,
    eval_env: bool = False,
    loader: Optional[Union[Type[SafeLoader], Type[UnsafeLoader]]] = None,
):
    """Yaml Wrapper for reading yaml files in a generic way."""
    files = _to_map(files)
    sections = _to_map(sections)
    keys = _to_map(keys)
    defaults = _to_map(defaults)

    if eval_env:
        defaults.update(
            {
                key: var
                for key, value in keys.items()
                if (
                    var := (
                        env_var
                        if isinstance(value, str) and (env_var := environ.get(value))
                        else env_vars[-1]
                        if (
                            env_vars := [
                                env_var
                                for sub_value in value
                                if isinstance(value, list) and (env_var := environ.get(sub_value))
                            ]
                        )
                        else None
                    )
                )
            }
        )

    config: dict = {}
    for file_key, file_names in files.items():
        if not file_key:
            if isinstance(file_names, str):
                recursive_update(config, _yaml_read(file_names, sections, keys, defaults, loader))
                return config

            for file in file_names:
                recursive_update(config, _yaml_read(file, sections, keys, defaults, loader))
                return config

        if isinstance(file_names, str):
            recursive_update(config, {file_key: _yaml_read(file_names, sections, keys, defaults, loader)})
            return config

        for file in file_names:
            recursive_update(config, {file_key: _yaml_read(file, sections, keys, defaults, loader)})

    return config
