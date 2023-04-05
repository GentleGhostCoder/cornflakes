from typing import Any, Callable, List, Optional, Union, cast

from cornflakes.decorator import Index, funcat
from cornflakes.decorator._types import ConfigGroup, DataclassProtocol
from cornflakes.decorator.config._load_config_group import create_group_loader
from cornflakes.decorator.dataclass import dataclass


def config_group(
    config_cls=None,
    files: Optional[Union[str, List[str]]] = None,
    allow_empty: Optional[bool] = None,
    chain_files: Optional[bool] = False,
    filter_function: Optional[Callable[..., bool]] = None,
    **kwargs,
) -> Union[Union[ConfigGroup, Any], Callable[..., Union[ConfigGroup, Any]]]:
    """Config decorator with a Subset of configs to parse Ini Files.

    :param config_cls: Config class
    :param files: Default config files
    :param allow_empty: Flag that allows empty config result
    :param chain_files: flag indicating whether to chain files in to single config.
    :param filter_function: Optional filter method for config
    :param kwargs: Additional args for custom dataclass. (dict_factory, eval_env. ...).

    :returns: wrapped class or the wrapper itself with the custom default arguments if the config class is not

    """
    files = files if isinstance(files, list) else [files] if files else []

    kwargs.pop("validate", None)  # no validation for group

    def wrapper(cls) -> Union[ConfigGroup, Any]:
        cls: Union[ConfigGroup, DataclassProtocol, Any] = dataclass(cls, **kwargs)
        cls.__config_files__ = files
        cls.__chain_files__ = chain_files
        cls.__allow_empty_config__ = allow_empty
        cls.__config_filter_function__ = filter_function

        cls.from_file = staticmethod(funcat(Index.reset, funcat_where="wrap")(create_group_loader(cls=cls)))

        return cast(ConfigGroup, cls)

    if config_cls:
        return wrapper(config_cls)
    return wrapper
