from typing import Callable, List, Optional, Type, Union, cast

from cornflakes.decorator._types import _T, ConfigGroup, DataclassProtocol
from cornflakes.decorator.config._load_config_group import create_group_loader
from cornflakes.decorator.dataclass import dataclass


def config_group(  # noqa: C901
    config_cls=None,
    files: Optional[Union[str, List[str]]] = None,
    allow_empty: Optional[bool] = False,
    filter_function: Optional[Callable[..., bool]] = None,
    **kwargs,
) -> Union[Union[ConfigGroup, DataclassProtocol], Callable[..., Union[ConfigGroup, DataclassProtocol]]]:
    """Config decorator with a Subset of configs to parse Ini Files.

    :param config_cls: Config class
    :param files: Default config files
    :param allow_empty: Flag that allows empty config result
    :param filter_function: Optional filter method for config
    :param kwargs: Additional args for custom dataclass. (dict_factory, eval_env. ...).

    :returns: wrapped class or the wrapper itself with the custom default arguments if the config class is not

    """
    files = files if isinstance(files, list) else [files] if files else []

    kwargs.pop("validate", None)  # no validation for group

    def wrapper(cls: Type[_T]) -> Union[DataclassProtocol, ConfigGroup]:
        cls = dataclass(cls, **kwargs)
        cls.__config_files__ = files
        cls.__allow_empty_config__ = allow_empty
        cls.__config_filter_function__ = filter_function
        cls.__ignored_slots__ = [
            key for key, value in cls.__dataclass_fields__.items() if getattr(value, "ignore", False)
        ]

        # Check __annotations__
        if not hasattr(cls, "__annotations__"):
            return cls

        cls = cast(ConfigGroup, cls)

        cls.from_file = staticmethod(create_group_loader(cls=cls))

        return cast(ConfigGroup, cls)

    if config_cls:
        return wrapper(config_cls)
    return wrapper
