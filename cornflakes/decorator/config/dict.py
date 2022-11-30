from dataclasses import asdict, is_dataclass
import os
from typing import Any, Callable, Dict, List, Optional, Union

from cornflakes.decorator._types import Config
from cornflakes.decorator.config._load_config import create_file_loader


def to_dict(self) -> Any:
    """Method to convert Dataclass with slots to dict."""
    if not is_dataclass(self):
        return self
    new_dict = asdict(self, dict_factory=getattr(self, "__dict_factory__", dict))
    if not any(
        [
            is_dataclass(value.type) or value.default_factory == list or isinstance(value.default, list)
            for value in getattr(self, "__dataclass_fields__", {}).values()
        ]
    ):
        return new_dict
    for key in getattr(self, "__slots__", getattr(self, "__dict__", {}).keys()):
        if is_dataclass(value := getattr(self, key)):
            new_dict.update({key: value.to_dict()})
        if isinstance(value, list) or isinstance(value, tuple):
            value = list(value)  # if tuple cast  to list
            for idx, sub_value in enumerate(value):
                if is_dataclass(sub_value):
                    value[idx] = sub_value.to_dict()
            new_dict.update({key: value})
    return new_dict


def create_dict_file_loader(
    cls=None,
) -> Callable[..., Dict[str, Optional[Union[Config, List[Config]]]]]:
    """Method to create file loader for ini files."""

    def from_dict(*args, config_dict=None, **kwargs) -> Dict[str, Optional[Union[Config, List[Config]]]]:
        if not config_dict:
            config_dict = {}
        default_kwargs = {}
        if cls.__eval_env__:
            default_kwargs.update(
                {key: os.environ[key] for key in cls.__dataclass_fields__.keys() if key in os.environ.keys()}
            )
        default_kwargs.update(kwargs)
        return create_file_loader(cls=cls)(*args, config_dict=config_dict, **default_kwargs)

    return from_dict


# def create_dict_group_loader(
#     cls=None,
# ) -> Callable[..., ConfigGroup]:
#     """Method to create file loader for ini files."""
#
#     def from_dict(*args, config_dict=None, **kwargs) -> ConfigGroup:
#         if not config_dict:
#             config_dict = {}
#         default_kwargs = {}
#         if cls.__eval_env__:
#             default_kwargs.update({key: os.environ[key] for key in cls.__dataclass_fields__.keys()
#                                    if key in os.environ.keys()})
#         default_kwargs.update(kwargs)
#         return create_group_loader(cls=cls)(*args, config_dict=config_dict, **default_kwargs)
#
#     return from_dict
