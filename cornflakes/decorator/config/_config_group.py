from dataclasses import dataclass
from typing import Callable, List, Union

from cornflakes.decorator._add_dataclass_slots import add_slots
from cornflakes.decorator.config._dict import create_dict_group_loader, to_dict
from cornflakes.decorator.config._ini import create_ini_group_loader, to_ini, to_ini_bytes
from cornflakes.decorator.config._loader import Loader
from cornflakes.decorator.config._protocols import ConfigGroup
from cornflakes.decorator.config._yaml import create_yaml_group_loader, to_yaml, to_yaml_bytes


def config_group(  # noqa: C901
    config_cls=None,
    files: Union[str, List[str]] = None,
    default_loader: Loader = Loader.INI_LOADER,
    allow_empty: bool = False,
    filter_function: Callable[..., bool] = None,
    *args,
    **kwargs,
) -> Callable[..., ConfigGroup]:
    """Config decorator with a Subset of configs to parse Ini Files.

    :param config_cls: Config class
    :param files: Default config files
    :param default_loader: Default config parser method (enum)
    :param args: Default configs to overwrite dataclass args
    :param kwargs: Default configs to overwrite dataclass args
    :param allow_empty: Flag that allows empty config result
    :param filter_function: Optional filter method for config

    :returns: wrapped class or the wrapper itself with the custom default arguments if the config class is not

    """

    def wrapper(cls) -> ConfigGroup:

        cls = add_slots(dataclass(cls, *args, **kwargs))
        cls.__config_files__ = files if isinstance(files, list) else [files]
        cls.__allow_empty_config__ = allow_empty
        cls.__config_filter_function__ = filter_function

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
        cls.from_file = getattr(cls, str(default_loader.value), cls.from_ini)

        return cls

    if config_cls:
        return wrapper(config_cls)
    return wrapper
