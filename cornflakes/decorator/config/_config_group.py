from typing import Callable, List, Optional, Union

from cornflakes.decorator import Index, funcat
from cornflakes.decorator.config._load_config_group import create_group_loader
from cornflakes.decorator.dataclass import dataclass
from cornflakes.decorator.types import ConfigGroup, Constants, Dataclass


def config_group(
    config_cls=None,
    files: Optional[Union[str, List[str]]] = None,
    allow_empty: Optional[bool] = None,
    chain_files: Optional[bool] = False,
    filter_function: Optional[Callable[..., bool]] = None,
    **kwargs,
) -> Union[Union[Dataclass, ConfigGroup], Callable[..., Union[Dataclass, ConfigGroup]]]:
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

    def wrapper(cls) -> Union[Dataclass, ConfigGroup]:
        cls = dataclass(cls, **kwargs)
        setattr(cls, Constants.config_decorator.FILES, files)
        setattr(cls, Constants.config_decorator.CHAIN_FILES, chain_files)
        setattr(cls, Constants.config_decorator.ALLOW_EMPTY, allow_empty)
        setattr(cls, Constants.config_decorator.FILTER_FUNCTION, filter_function)
        cls.from_file = staticmethod(funcat(Index.reset, funcat_where="wrap")(create_group_loader(cls=cls)))

        return cls

    return wrapper(config_cls) if config_cls else wrapper
