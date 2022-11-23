from typing import Callable, Dict, List, Optional, Type, Union

import yaml
from yaml import SafeLoader, UnsafeLoader

from cornflakes.decorator.config._load_config import create_file_loader
from cornflakes.decorator.config._load_config_group import create_group_loader
from cornflakes.decorator.config._protocols import Config, ConfigGroup
from cornflakes.decorator.config._write_config import write_config
from cornflakes.parser import yaml_load


def specific_yaml_loader(loader: Union[Type[SafeLoader], Type[UnsafeLoader]] = SafeLoader):
    """Wrapper method to predefine yaml loader parameter."""

    def _yaml_loader(*args, **kwargs):
        return yaml_load(*args, loader=loader, **kwargs)

    return _yaml_loader


def to_yaml_bytes(self, *args, **kwargs):
    """Method to write an instance of the main config class of the module into a yaml bytearray."""
    return yaml.dump({self.__class__.__name__.lower(): self.to_dict()}, *args, **kwargs).encode("utf-8")


def to_yaml(self, out_cfg: Optional[str] = None, *args, **kwargs) -> Optional[bytearray]:
    """Method to write an instance of the main config class of the module into a yaml file."""
    return write_config(self.to_yaml_bytes(*args, **kwargs), out_cfg)


def create_yaml_file_loader(
    cls=None,
) -> Callable[..., Dict[str, Optional[Union[Config, List[Config]]]]]:
    """Method to create file loader for yaml files."""

    def from_yaml(
        *args, loader: Union[Type[SafeLoader], Type[UnsafeLoader]] = SafeLoader, **kwargs
    ) -> Dict[str, Optional[Union[Config, List[Config]]]]:
        _from_yaml = create_file_loader(cls=cls, loader=specific_yaml_loader(loader=loader))  # type: ignore
        return _from_yaml(*args, **kwargs)

    return from_yaml


def create_yaml_group_loader(
    cls=None,
) -> Callable[..., ConfigGroup]:
    """Method to create file loader for yaml files."""

    def from_yaml(*args, loader: Union[Type[SafeLoader], Type[UnsafeLoader]] = SafeLoader, **kwargs) -> ConfigGroup:
        _from_yaml = create_group_loader(cls=cls, loader=specific_yaml_loader(loader=loader))  # type: ignore
        return _from_yaml(*args, **kwargs)

    return from_yaml
