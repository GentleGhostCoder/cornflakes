from typing import Any, Dict, List, Optional, Protocol, Tuple, Union


class Config(Protocol):
    """Config Protocol Type."""

    __dataclass_fields__: dict
    __dataclass_params__: dict
    __config_sections__: str
    __config_files__: str
    __multi_config__: str
    __config_list__: str
    __args__: List[Any]
    __slots__: Tuple[str]

    def __call__(self, *args, **kwargs) -> Any:
        """Call Function."""
        ...

    def __config_filter_function__(self) -> bool:
        """Callback function to filter config."""
        ...

    def to_dict(self, *args, **kwargs) -> dict:
        """Parse config to dict."""
        ...

    def to_ini(self, *args, **kwargs) -> Union[bytearray, None]:
        """Parse config to ini file / bytes."""
        ...

    def to_yaml(self, *args, **kwargs) -> Union[bytearray, None]:
        """Parse config to yaml file / bytes."""
        ...

    def to_yaml_bytes(self, *args, **kwargs) -> bytearray:
        """Parse config to yaml bytes."""
        ...

    def to_ini_bytes(self, *args, **kwargs) -> bytearray:
        """Parse config to ini bytes."""
        ...

    @staticmethod
    def from_ini(
        files: Optional[Union[Dict[Optional[str], Union[List[str], str]], List[str], str]] = None,
        sections: Optional[Union[Dict[Optional[str], Union[List[str], str]], List[str], str]] = None,
        keys: Optional[Union[Dict[Optional[str], Union[List[str], str]], List[str], str]] = None,
        defaults: Optional[Union[Dict[Optional[str], Union[List[str], str]], List[str], str]] = None,
        *args,
        **kwargs
    ) -> Any:
        """Parse ini file to config."""
        ...

    @staticmethod
    def from_yaml(
        files: Optional[Union[Dict[Optional[str], Union[List[str], str]], List[str], str]] = None,
        sections: Optional[Union[Dict[Optional[str], Union[List[str], str]], List[str], str]] = None,
        keys: Optional[Union[Dict[Optional[str], Union[List[str], str]], List[str], str]] = None,
        defaults: Optional[Union[Dict[Optional[str], Union[List[str], str]], List[str], str]] = None,
        *args,
        **kwargs
    ) -> Any:
        """Parse yaml file to config."""
        ...

    @staticmethod
    def from_dict(
        files: Optional[Union[Dict[Optional[str], Union[List[str], str]], List[str], str]] = None,
        sections: Optional[Union[Dict[Optional[str], Union[List[str], str]], List[str], str]] = None,
        keys: Optional[Union[Dict[Optional[str], Union[List[str], str]], List[str], str]] = None,
        defaults: Optional[Union[Dict[Optional[str], Union[List[str], str]], List[str], str]] = None,
        *args,
        **kwargs
    ) -> Any:
        """Parse dict to config."""
        ...

    @staticmethod
    def from_file(
        files: Optional[Union[Dict[Optional[str], Union[List[str], str]], List[str], str]] = None,
        sections: Optional[Union[Dict[Optional[str], Union[List[str], str]], List[str], str]] = None,
        keys: Optional[Union[Dict[Optional[str], Union[List[str], str]], List[str], str]] = None,
        defaults: Optional[Union[Dict[Optional[str], Union[List[str], str]], List[str], str]] = None,
        *args,
        **kwargs
    ) -> Any:
        """Parse file to config."""
        ...


class ConfigGroup(Protocol):
    """ConfigGroup Protocol Type."""

    __dataclass_fields__: dict
    __dataclass_params__: dict
    __config_sections__: str
    __config_files__: str
    __multi_config__: str
    __config_list__: str
    __args__: List[Any]
    __slots__: Tuple[str]

    def __call__(self, *args, **kwargs) -> Any:
        """Call Function."""
        ...

    def __config_filter_function__(self) -> bool:
        """Callback function to filter config."""
        ...

    def to_dict(self, *args, **kwargs) -> dict:
        """Parse config to dict."""
        ...

    def to_ini(self, *args, **kwargs) -> Union[bytearray, None]:
        """Parse config to ini file / bytes."""
        ...

    def to_yaml(self, *args, **kwargs) -> Union[bytearray, None]:
        """Parse config to yaml file / bytes."""
        ...

    def to_yaml_bytes(self, *args, **kwargs) -> bytearray:
        """Parse config to yaml bytes."""
        ...

    def to_ini_bytes(self, *args, **kwargs) -> bytearray:
        """Parse config to ini bytes."""
        ...

    @staticmethod
    def from_ini(
        files: Optional[Union[Dict[Optional[str], Union[List[str], str]], List[str], str]] = None,
        sections: Optional[Union[Dict[Optional[str], Union[List[str], str]], List[str], str]] = None,
        keys: Optional[Union[Dict[Optional[str], Union[List[str], str]], List[str], str]] = None,
        defaults: Optional[Union[Dict[Optional[str], Union[List[str], str]], List[str], str]] = None,
        *args,
        **kwargs
    ) -> Any:
        """Parse ini file to config."""
        ...

    @staticmethod
    def from_yaml(
        files: Optional[Union[Dict[Optional[str], Union[List[str], str]], List[str], str]] = None,
        sections: Optional[Union[Dict[Optional[str], Union[List[str], str]], List[str], str]] = None,
        keys: Optional[Union[Dict[Optional[str], Union[List[str], str]], List[str], str]] = None,
        defaults: Optional[Union[Dict[Optional[str], Union[List[str], str]], List[str], str]] = None,
        *args,
        **kwargs
    ) -> Any:
        """Parse yaml file to config."""
        ...

    @staticmethod
    def from_dict(
        files: Optional[Union[Dict[Optional[str], Union[List[str], str]], List[str], str]] = None,
        sections: Optional[Union[Dict[Optional[str], Union[List[str], str]], List[str], str]] = None,
        keys: Optional[Union[Dict[Optional[str], Union[List[str], str]], List[str], str]] = None,
        defaults: Optional[Union[Dict[Optional[str], Union[List[str], str]], List[str], str]] = None,
        *args,
        **kwargs
    ) -> Any:
        """Parse dict to config."""
        ...

    @staticmethod
    def from_file(
        files: Optional[Union[Dict[Optional[str], Union[List[str], str]], List[str], str]] = None,
        sections: Optional[Union[Dict[Optional[str], Union[List[str], str]], List[str], str]] = None,
        keys: Optional[Union[Dict[Optional[str], Union[List[str], str]], List[str], str]] = None,
        defaults: Optional[Union[Dict[Optional[str], Union[List[str], str]], List[str], str]] = None,
        *args,
        **kwargs
    ) -> Any:
        """Parse file to config."""
        ...
