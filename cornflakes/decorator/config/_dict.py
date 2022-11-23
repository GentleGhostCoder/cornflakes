from dataclasses import asdict
from functools import partial
from typing import Callable, Dict, List, Optional, Union

from cornflakes.decorator.config._load_config import create_file_loader
from cornflakes.decorator.config._load_config_group import create_group_loader
from cornflakes.decorator.config._protocols import Config, ConfigGroup


def __dict_factory(ignored, items):
    return {key: value for key, value in items if key not in ignored}


def to_dict(self) -> dict:
    """Method to convert Dataclass with slots to dict."""
    return asdict(self, dict_factory=partial(__dict_factory, self.__ignored_slots__))


def create_dict_file_loader(
    cls=None,
) -> Callable[..., Dict[str, Optional[Union[Config, List[Config]]]]]:
    """Method to create file loader for ini files."""

    def from_dict(*args, config_dict, **kwargs) -> Dict[str, Optional[Union[Config, List[Config]]]]:
        return create_file_loader(cls=cls)(*args, config_dict=config_dict, **kwargs)

    return from_dict


def create_dict_group_loader(
    cls=None,
) -> Callable[..., ConfigGroup]:
    """Method to create file loader for ini files."""

    def from_dict(*args, config_dict, **kwargs) -> ConfigGroup:
        return create_group_loader(cls=cls)(*args, config_dict=config_dict, **kwargs)

    return from_dict
