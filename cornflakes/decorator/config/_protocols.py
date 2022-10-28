from typing import Any, Callable, Dict, List, Optional, Protocol, TypeVar, Union


class BaseConfig(Protocol):
    """Config Protocol Type."""

    __dataclass_fields__: dict = None
    __dataclass_params__: dict = None
    __call__: Callable[..., Any]
    __config_sections__: str = None
    __config_files__: str = None
    __multi_config__: str = None
    __config_list__: str = None
    to_dict: Callable
    to_ini: Callable
    to_yaml: Callable
    to_yaml_bytes: Callable
    to_ini_bytes: Callable
    from_yaml: Callable
    from_ini: Callable  # class not dependent method
    from_dict: Callable
    from_file: Callable


ConfigLoader = TypeVar(
    "ConfigLoader",
    bound=Callable[
        [
            Union[str, List[str], Dict[Union[str, None], Union[str, List[str]]]],
            Optional[Union[str, List[str], Dict[Union[str, None], Union[str, List[str]]]]],
            Optional[Union[str, List[str], Dict[Union[str, None], Union[str, List[str]]]]],
            Optional[Union[str, List[str], Dict[str, Any]]],
            Optional[Any],
        ],
        BaseConfig,
    ],
)

ToDict = TypeVar(
    "ToDict",
    bound=Callable[
        [
            Union[str, List[str], Dict[Union[str, None], Union[str, List[str]]]],
            Optional[Union[str, List[str], Dict[Union[str, None], Union[str, List[str]]]]],
            Optional[Union[str, List[str], Dict[Union[str, None], Union[str, List[str]]]]],
            Optional[Union[str, List[str], Dict[str, Any]]],
            Optional[Any],
        ],
        dict,
    ],
)

ToBytes = TypeVar(
    "ToBytes",
    bound=Callable[
        [
            Union[str, List[str], Dict[Union[str, None], Union[str, List[str]]]],
            Optional[Union[str, List[str], Dict[Union[str, None], Union[str, List[str]]]]],
            Optional[Union[str, List[str], Dict[Union[str, None], Union[str, List[str]]]]],
            Optional[Union[str, List[str], Dict[str, Any]]],
            Optional[Any],
        ],
        bytearray,
    ],
)

ConfigWriter = TypeVar(
    "ConfigWriter",
    bound=Callable[
        [
            Union[str, List[str], Dict[Union[str, None], Union[str, List[str]]]],
            Optional[Union[str, List[str], Dict[Union[str, None], Union[str, List[str]]]]],
            Optional[Union[str, List[str], Dict[Union[str, None], Union[str, List[str]]]]],
            Optional[Union[str, List[str], Dict[str, Any]]],
            Optional[Any],
        ],
        dict,
    ],
)


class Config(Protocol):
    """Config Protocol Type."""

    __dataclass_fields__: dict = None
    __dataclass_params__: dict = None
    __call__: Callable[..., Any]
    __config_sections__: str = None
    __config_files__: str = None
    __multi_config__: str = None
    __config_list__: str = None
    to_dict: ToDict
    to_ini: ConfigWriter
    to_yaml: ConfigWriter
    to_yaml_bytes: ToBytes
    to_ini_bytes: ToBytes
    from_yaml: ConfigLoader
    from_ini: ConfigLoader  # class not dependent method
    from_dict: ConfigLoader
    from_file: ConfigLoader


ConfigGroupLoader = TypeVar(
    "ConfigGroupLoader",
    bound=Callable[
        [
            Union[str, List[str], Dict[Union[str, None], Union[str, List[str]]]],
            Optional[Union[str, List[str], Dict[Union[str, None], Union[str, List[str]]]]],
            Optional[Union[str, List[str], Dict[Union[str, None], Union[str, List[str]]]]],
            Optional[Union[str, List[str], Dict[str, Any]]],
            Optional[Any],
        ],
        Config,
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
    to_dict: ToDict
    to_ini: ConfigWriter
    to_yaml: ConfigWriter
    to_yaml_bytes: ToBytes
    to_ini_bytes: ToBytes
    from_yaml: ConfigGroupLoader
    from_ini: ConfigGroupLoader  # class not dependent method
    from_dict: ConfigGroupLoader
    from_file: ConfigGroupLoader
