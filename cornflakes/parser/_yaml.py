import collections.abc
from os.path import abspath, expanduser
from typing import Any, Dict, List, Optional, Union

import yaml
from yaml import SafeLoader, UnsafeLoader


def _update(d, u):
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = _update(d.get(k, {}), v)
        else:
            d[k] = v
    return d


def _get_updated_key(config: Dict, values: List[str], defaults: Dict):
    result = None
    key = None
    for value in values:
        key = config.get(value, defaults.get(value, None))
        if key:
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
    config: Dict,
    keys: Optional[Union[str, List[str], Dict[Union[str, None], Union[str, List[str]]]]],
    defaults: Optional[Union[str, List[str], Dict[str, Any]]],
) -> Dict:
    return {sub_key: _get_values(config, sub_value, defaults) for sub_key, sub_value in keys.items()}


def _get_all_sections(
    config: Dict,
    sections: Optional[Union[str, List[str], Dict[Union[str, None], Union[str, List[str]]]]],
    keys: Optional[Union[str, List[str], Dict[Union[str, None], Union[str, List[str]]]]],
    defaults: Optional[Union[str, List[str], Dict[str, Any]]],
) -> Dict:
    new_config = {}
    for section_key, section_names in sections.items():
        if not section_key:
            if isinstance(section_names, str):
                _update(new_config, _get_section(config.get(section_names, {}), keys, defaults))
                continue
            for section in section_names:
                _update(new_config, _get_section(config.get(section, {}), keys, defaults))
        if isinstance(section_names, str):
            _update(new_config, {section_key: _get_section(config.get(section_names, {}), keys, defaults)})
            continue
        for section in section_names:
            _update(new_config, {section_key: _get_section(config.get(section, {}), keys, defaults)})
    return new_config


def _yaml_read(
    file: str,
    sections: Optional[Union[str, List[str], Dict[Union[str, None], Union[str, List[str]]]]],
    keys: Optional[Union[str, List[str], Dict[Union[str, None], Union[str, List[str]]]]],
    defaults: Optional[Union[str, List[str], Dict[str, Any]]],
    loader: Optional[Union[UnsafeLoader, SafeLoader]],
) -> Dict:
    with open(abspath(expanduser(file)), "rb") as f:
        data = f.read()
        if not loader:
            loader = yaml.UnsafeLoader if b": !!" in data else yaml.SafeLoader
        config = yaml.load(data, Loader=loader)  # noqa: S506
        if not sections:
            if not keys:
                return config
            if not defaults:
                defaults = keys
            return _get_all_sections(config, _to_map(list(config.keys())), keys, defaults)
        return _get_all_sections(config, sections, keys, defaults)


def _to_map(obj: Union[str, List[str], Dict[str, Union[str, List[str]]], None]) -> Dict[str, Union[str, List[str]]]:
    return (
        isinstance(obj, str)
        and {obj: obj}  # string
        or (isinstance(obj, list) or isinstance(obj, tuple))
        and {key: key for key in obj}  # list
        or obj
        or {}
    )  # dict


def yaml_load(
    files: Union[str, List[str], Dict[Union[str, None], Union[str, List[str]]]],
    sections: Optional[Union[str, List[str], Dict[Union[str, None], Union[str, List[str]]]]] = None,
    keys: Optional[Union[str, List[str], Dict[Union[str, None], Union[str, List[str]]]]] = None,
    defaults: Optional[Union[str, List[str], Dict[str, Any]]] = None,
    loader: Optional[Union[UnsafeLoader, SafeLoader]] = None,
):
    """Yaml Wrapper for reading yaml files in a generic way."""
    files = _to_map(files)
    sections = _to_map(sections)
    keys = _to_map(keys)
    defaults = _to_map(defaults)

    config = {}
    for file_key, file_names in files.items():
        if not file_key:
            _update(config, _yaml_read(file_names, sections, keys, defaults, loader))

        if isinstance(file_names, str):
            _update(config, {file_key: _yaml_read(file_names, sections, keys, defaults, loader)})
            return config

        for file in file_names:
            _update(config, {file_key: _yaml_read(file, sections, keys, defaults, loader)})

    return config


def specific_yaml_loader(loader: Union[yaml.SafeLoader, yaml.UnsafeLoader] = yaml.SafeLoader):
    """Wrapper method to predefine yaml loader parameter."""

    def _yaml_loader(*args, **kwargs):
        return yaml_load(*args, loader=loader, **kwargs)

    return _yaml_loader
