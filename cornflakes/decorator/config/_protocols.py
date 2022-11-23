from typing import Any, Dict, List, Optional, Protocol, Tuple, Union


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


class Config(Protocol):
    """Config Protocol Type."""

    __dataclass_fields__: dict
    __dataclass_params__: dict
    __config_sections__: Union[Dict[Optional[str], Union[List[str], str]], List[str], str]
    __config_files__: Union[Dict[Optional[str], Union[List[str], str]], List[str], str]
    __ignored_slots__: List[str]
    __multi_config__: bool
    __config_list__: bool
    __args__: List[Any]
    __slots__: Tuple[str]
    __eval_env__: bool = None

    def __call__(self, *args, **kwargs) -> Any:
        """Call Function."""
        ...

    def __config_filter_function__(self) -> bool:
        """Callback function to filter config."""
        ...

    def to_dict(self, *args, **kwargs) -> dict:
        """Parse config to dict."""
        ...

    def to_ini(self, *args, **kwargs) -> Optional[bytearray]:
        """Parse config to ini file / bytes."""
        ...

    def to_yaml(self, *args, **kwargs) -> Optional[bytearray]:
        """Parse config to yaml file / bytes."""
        ...

    def to_yaml_bytes(self, *args, **kwargs) -> bytearray:
        """Parse config to yaml bytes."""
        ...

    def to_ini_bytes(self, *args, **kwargs) -> bytearray:
        """Parse config to ini bytes."""
        ...

    from_ini: LoaderMethod
    from_yaml: LoaderMethod
    from_dict: LoaderMethod
    from_file: LoaderMethod


class ConfigGroup(Protocol):
    """ConfigGroup Protocol Type."""

    __dataclass_fields__: dict
    __dataclass_params__: dict
    __config_files__: Union[Dict[Optional[str], Union[List[str], str]], List[str], str]
    __multi_config__: bool
    __config_list__: bool
    __args__: List[Any]
    __slots__: Tuple[str]
    __eval_env__: bool = None

    def __call__(self, *args, **kwargs) -> Any:
        """Call Function."""
        ...

    def __config_filter_function__(self) -> bool:
        """Callback function to filter config."""
        ...

    def to_dict(self, *args, **kwargs) -> dict:
        """Parse config to dict."""
        ...

    def to_ini(self, *args, **kwargs) -> Optional[bytearray]:
        """Parse config to ini file / bytes."""
        ...

    def to_yaml(self, *args, **kwargs) -> Optional[bytearray]:
        """Parse config to yaml file / bytes."""
        ...

    def to_yaml_bytes(self, *args, **kwargs) -> bytearray:
        """Parse config to yaml bytes."""
        ...

    def to_ini_bytes(self, *args, **kwargs) -> bytearray:
        """Parse config to ini bytes."""
        ...

    from_ini: LoaderMethod
    from_yaml: LoaderMethod
    from_dict: LoaderMethod
    from_file: LoaderMethod
