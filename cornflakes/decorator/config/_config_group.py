from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Union

from cornflakes import ini_load
from cornflakes.decorator._add_dataclass_slots import add_slots
from cornflakes.decorator.config._dict import create_dict_group_loader, to_dict
from cornflakes.decorator.config._ini import create_ini_group_loader, to_ini, to_ini_bytes
from cornflakes.decorator.config._yaml import create_yaml_group_loader, to_yaml, to_yaml_bytes


def config_group(  # noqa: C901
    config_cls=None,
    files: Union[str, List[str]] = None,
    *args,
    loader: Callable[
        [
            Union[
                Union[str, List[str], Dict[Union[str, None], Union[str, List[str]]]],
                Optional[Union[str, List[str], Dict[Union[str, None], Union[str, List[str]]]]],
                Optional[Union[str, List[str], Dict[Union[str, None], Union[str, List[str]]]]],
                Optional[Union[str, List[str], Dict[str, Any]]],
            ]
        ],
        Dict,
    ] = ini_load,
    **kwargs,
):
    """Config decorator with a Subset of configs to parse Ini Files.

    :param config_cls: Config class
    :param files: Default config files
    :param loader: Config Loader (ini_load, yaml_load)
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

        def _new(self, *new_args, **new_kwargs):
            # two chars missing in original of next line ...
            self.to_dict = to_dict
            self.to_ini = to_ini
            self.to_yaml = to_yaml
            self.to_yaml_bytes = to_yaml_bytes
            self.to_ini_bytes = to_ini_bytes
            return super(cls, self).__new__(self)

        cls.__new__ = classmethod(_new)

        cls.from_yaml = staticmethod(create_yaml_group_loader(cls=cls))
        cls.from_ini = staticmethod(create_ini_group_loader(cls=cls))  # class not dependent method
        cls.from_dict = staticmethod(create_dict_group_loader(cls=cls))

        return cls

    if config_cls:
        return wrapper(config_cls)
    return wrapper
