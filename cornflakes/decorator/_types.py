from typing import Any, Callable, ClassVar, Dict, List, Optional, Protocol, TypeVar, Union

_T = TypeVar("_T")


class _WithoutDefault:
    pass


WITHOUT_DEFAULT = _WithoutDefault()


class LoaderMethod(Protocol):
    """Config loader method protocol."""

    @staticmethod
    def __call__(
        files: Optional[Union[Dict[Optional[str], Union[List[str], str]], List[str], str]] = None,
        sections: Optional[Union[Dict[Optional[str], Union[List[str], str]], List[str], str]] = None,
        keys: Optional[Union[Dict[Optional[str], Union[List[str], str]], List[str], str]] = None,
        defaults: Optional[Union[Dict[Optional[str], Union[List[str], str]], List[str], str]] = None,
        eval_env: bool = False,
        *args,
        **kwargs
    ) -> Any:
        """Config loader method protocol."""
        ...


class DataclassProtocol(Protocol):
    """Dataclass protocol custom implementation."""

    # stdlib attributes
    __dataclass_fields__: ClassVar[Dict[str, Any]]
    __dataclass_params__: ClassVar[Dict]  # in reality `dataclasses._DataclassParams`
    __post_init__: ClassVar[Optional[Callable[..., None]]]
    # _FIELDS: ClassVar[]
    __args__: ClassVar[List[Any]]
    # custom
    __eval_env__: bool = None

    def __call__(self, *args, **kwargs) -> Any:
        """Call Function."""
        ...


class Config(DataclassProtocol):
    """Config Protocol Type."""

    __config_sections__: ClassVar[Union[Dict[Optional[str], Union[List[str], str]], List[str], str]]
    __config_files__: ClassVar[Union[Dict[Optional[str], Union[List[str], str]], List[str], str]]
    __ignored_slots__: ClassVar[List[str]]
    __multi_config__: ClassVar[bool]
    __config_list__: ClassVar[bool]
    __allow_empty_config__: ClassVar[bool]

    def __call__(self, *args, **kwargs) -> Any:
        """Call Function."""
        ...

    def __config_filter_function__(self) -> bool:
        """Callback function to filter config."""
        ...

    def to_dict(self, *args, **kwargs) -> Any:
        """Parse config to dict."""
        ...

    def to_tuple(self, *args, **kwargs) -> Any:
        """Parse config to tuple."""
        ...

    def to_ini(self, *args, **kwargs) -> Optional[bytearray]:
        """Parse config to ini file / bytes."""
        ...

    def to_yaml(self, *args, **kwargs) -> Optional[bytearray]:
        """Parse config to yaml file / bytes."""
        ...

    def to_yaml_bytes(self, *args, **kwargs) -> Optional[bytearray]:
        """Parse config to yaml bytes."""
        ...

    def to_ini_bytes(self, *args, **kwargs) -> Optional[bytearray]:
        """Parse config to ini bytes."""
        ...

    from_ini: LoaderMethod
    from_yaml: LoaderMethod
    from_dict: LoaderMethod
    from_file: LoaderMethod


class ConfigGroup(DataclassProtocol):
    """ConfigGroup Protocol Type."""

    __config_files__: ClassVar[Union[Dict[Optional[str], Union[List[str], str]], List[str], str]]
    __multi_config__: ClassVar[bool]
    __config_list__: ClassVar[bool]
    __allow_empty_config__: ClassVar[bool]

    def __call__(self, *args, **kwargs) -> Any:
        """Call Function."""
        ...

    def __config_filter_function__(self) -> bool:
        """Callback function to filter config."""
        ...

    def to_dict(self, *args, **kwargs) -> Any:
        """Parse config to dict."""
        ...

    def to_tuple(self, *args, **kwargs) -> Any:
        """Parse config to tuple."""
        ...

    def to_ini(self, *args, **kwargs) -> Optional[bytearray]:
        """Parse config to ini file / bytes."""
        ...

    def to_yaml(self, *args, **kwargs) -> Optional[bytearray]:
        """Parse config to yaml file / bytes."""
        ...

    def to_yaml_bytes(self, *args, **kwargs) -> Optional[bytearray]:
        """Parse config to yaml bytes."""
        ...

    def to_ini_bytes(self, *args, **kwargs) -> Optional[bytearray]:
        """Parse config to ini bytes."""

    ...

    from_ini: LoaderMethod
    from_yaml: LoaderMethod
    from_dict: LoaderMethod
    from_file: LoaderMethod
