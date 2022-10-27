from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Protocol, TypeVar, Union

from cornflakes.decorator._add_dataclass_slots import add_slots
from cornflakes.decorator.config._dict import create_dict_group_loader, to_dict
from cornflakes.decorator.config._ini import create_ini_group_loader, to_ini, to_ini_bytes
from cornflakes.decorator.config._yaml import create_yaml_group_loader, to_yaml, to_yaml_bytes

F_loader = TypeVar(
    "F_loader",
    bound=Callable[
        [
            Union[str, List[str], Dict[Union[str, None], Union[str, List[str]]]],
            Optional[Union[str, List[str], Dict[Union[str, None], Union[str, List[str]]]]],
            Optional[Union[str, List[str], Dict[Union[str, None], Union[str, List[str]]]]],
            Optional[Union[str, List[str], Dict[str, Any]]],
            Optional[Any],
        ],
        Any,
    ],
)


class ConfigGroup(Protocol):
    """ConfigGroup Protocol Type."""

    __dataclass_fields__: dict = None
    __dataclass_params__: dict = None
    __call__: Callable[[...], Any] = None
    __config_sections__: str = None
    __config_files__: str = None
    __multi_config__: str = None
    __config_list__: str = None
    to_dict: F_loader
    to_ini: F_loader
    to_yaml: F_loader
    to_yaml_bytes: F_loader
    to_ini_bytes: F_loader
    from_yaml: F_loader
    from_ini: F_loader  # class not dependent method
    from_dict: F_loader


def config_group(  # noqa: C901
    config_cls=None,
    files: Union[str, List[str]] = None,
    *args,
    **kwargs,
) -> Callable[..., ConfigGroup]:
    """Config decorator with a Subset of configs to parse Ini Files.

    :param config_cls: Config class
    :param files: Default config files
    :param args: Default configs to overwrite dataclass args
    :param kwargs: Default configs to overwrite dataclass args

    :returns: wrapped class or the wrapper itself with the custom default arguments if the config class is not

    """

    def wrapper(cls):

        cls = add_slots(dataclass(cls, *args, **kwargs))
        cls.__config_files__ = files

        # Check __annotations__
        if not hasattr(cls, "__annotations__"):
            return cls

        def new(self, *new_args, **new_kwargs):
            # two chars missing in original of next line ...
            self.to_dict = to_dict
            self.to_ini = to_ini
            self.to_yaml = to_yaml
            self.to_yaml_bytes = to_yaml_bytes
            self.to_ini_bytes = to_ini_bytes
            return super(cls, self).__new__(self)

        cls.__new__ = classmethod(new)

        cls.from_yaml = staticmethod(create_yaml_group_loader(cls=cls))
        cls.from_ini = staticmethod(create_ini_group_loader(cls=cls))  # class not dependent method
        cls.from_dict = staticmethod(create_dict_group_loader(cls=cls))

        return cls

    if config_cls:
        return wrapper(config_cls)
    return wrapper
