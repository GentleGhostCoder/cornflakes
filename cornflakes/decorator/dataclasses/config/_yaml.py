from typing import Callable, Dict, List, Optional, Type, Union

import yaml
from yaml import SafeLoader, UnsafeLoader

from cornflakes.decorator.dataclasses.config._load_config import create_file_loader
from cornflakes.decorator.dataclasses.config._write_config import write_config
from cornflakes.parser import yaml_load
from cornflakes.types import Config


def specific_yaml_loader(loader: Union[Type[SafeLoader], Type[UnsafeLoader]] = SafeLoader):
    """Wrapper method to predefine yaml loader parameter."""

    def _yaml_loader(*args, **kwargs):
        return yaml_load(*args, loader=loader, **kwargs)

    return _yaml_loader


def to_yaml_bytes(self, *args, **kwargs) -> bytes:
    """Method to write an instance of the main config class of the module into a yaml bytearray."""
    return yaml.dump({self.__class__.__name__.lower(): self.to_dict()}, *args, **kwargs).encode("utf-8")


def to_yaml(self, *args, out_cfg: Optional[str] = None, **kwargs) -> Optional[bytearray]:
    """Method to write an instance of the main config class of the module into a yaml file."""
    # TODO: More Tests for nested Objects
    return write_config(bytearray(to_yaml_bytes(self, *args, **kwargs)), out_cfg)


def create_yaml_file_loader(
    cls,
) -> Callable[..., Dict[str, Optional[Union[Config, List[Config]]]]]:
    """Method to create file loader for yaml files."""

    def from_yaml(
        *args, loader: Union[Type[SafeLoader], Type[UnsafeLoader]] = SafeLoader, **kwargs
    ) -> Dict[str, Optional[Union[Config, List[Config]]]]:
        _from_yaml = create_file_loader(cls=cls, _loader_callback=specific_yaml_loader(loader=loader))  # type: ignore
        return _from_yaml(*args, **kwargs)

    return from_yaml
