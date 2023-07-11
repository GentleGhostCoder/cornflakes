from dataclasses import MISSING
from enum import Enum
from typing import Any, Callable, ClassVar, Dict, List, Optional, Protocol, TypeVar, Union, runtime_checkable

_T = TypeVar("_T")


class _WithoutDefault:
    pass


WITHOUT_DEFAULT = type(_WithoutDefault())
MISSING_TYPE = type(MISSING)


class Loader(Enum):
    """Config Loader Enums."""

    INI_LOADER = "from_ini"
    YAML_LOADER = "from_yaml"
    DICT_LOADER = "from_dict"
    FILE_LOADER = "from_file"


class ConfigArguments(Enum):
    """Config Arguments Enums."""

    files = "files"
    sections = "sections"
    use_regex = "use_regex"
    is_list = "is_list"
    default_loader = "default_loader"
    allow_empty = "allow_empty"
    filter_function = "filter_function"


ConfigArgument = Optional[Optional[Union[Dict[Optional[str], Union[List[str], str]], List[str], str]]]


@runtime_checkable
class LoaderMethod(Protocol):
    """Config loader method protocol."""

    @staticmethod
    def __call__(
        files: ConfigArgument = None,
        sections: ConfigArgument = None,
        keys: ConfigArgument = None,
        defaults: ConfigArgument = None,
        eval_env: bool = False,
        *args,
        **kwargs
    ) -> Any:
        """Config loader method protocol.


        Methods generated by the Methods implemented in:
        from_yaml -> :meth:`cornflakes.decorator.config.yaml.create_yaml_file_loader`
        from_ini -> :meth:`cornflakes.decorator.config.ini.create_ini_file_loader`
        from_dict -> :meth:`cornflakes.decorator.config.dict.create_dict_file_loader`
        """
        ...


@runtime_checkable
class DataclassProtocol(Protocol):
    """Dataclass protocol custom implementation."""

    # stdlib attributes
    __dataclass_fields__: ClassVar[Dict[str, Any]]
    __dataclass_params__: ClassVar[Dict]  # in reality `dataclasses._DataclassParams`
    __annotations__: ClassVar[Dict]
    __post_init__: ClassVar[Optional[Callable[..., None]]]
    # _FIELDS: ClassVar[]
    __args__: ClassVar[List[Any]]
    # custom
    __eval_env__: bool = None

    def __call__(self, *args, **kwargs) -> Any:
        """Call Function."""
        ...

    def to_dict(self, *args, **kwargs) -> Any:
        """Parse config to dict.

        Method implemented in :meth:`cornflakes.decorator.dataclass._dataclass.to_dict`.
        """
        ...

    def to_tuple(self, *args, **kwargs) -> Any:
        """Parse config to tuple.

        Method implemented in :meth:`cornflakes.decorator.dataclass._dataclass.to_tuple`.
        """
        ...

    def to_ini(self, *args, **kwargs) -> Optional[bytearray]:
        """Parse config to ini file / bytes.

        Method implemented in :meth:`cornflakes.decorator.config.ini.to_ini`.
        """
        ...

    def to_yaml(self, *args, **kwargs) -> Optional[bytearray]:
        """Parse config to yaml file / bytes.

        Method implemented in :meth:`cornflakes.decorator.config.yaml.to_yaml`.
        """
        ...

    def to_yaml_bytes(self, *args, **kwargs) -> Optional[bytearray]:
        """Parse config to yaml bytes.

        Method implemented in :meth:`cornflakes.decorator.config.yaml.to_yaml_bytes`.
        """
        ...

    def to_ini_bytes(self, *args, **kwargs) -> Optional[bytearray]:
        """Parse config to ini bytes.

        Method implemented in :meth:`cornflakes.decorator.config.ini.to_ini_bytes`.
        """
        ...

    def validate_kwargs(self, validate=False, **kwargs) -> Dict[str, Any]:
        """Validate kwargs.

        Method implemented in :meth:`cornflakes.decorator.dataclass._validate.validate_dataclass_kwargs`.
        """
        ...

    def check_kwargs(self, validate=False, **kwargs) -> Dict[str, Any]:
        """Check dataclass kwargs.

        Method implemented in :meth:`cornflakes.decorator.dataclass._validate.check_dataclass_kwargs`.
        """
        ...


@runtime_checkable
class Config(Protocol):
    """Config Protocol Type."""

    # stdlib attributes
    __dataclass_fields__: ClassVar[Dict[str, Any]]
    __dataclass_params__: ClassVar[Dict]  # in reality `dataclasses._DataclassParams`
    __annotations__: ClassVar[Dict]
    __post_init__: ClassVar[Optional[Callable[..., None]]]
    # _FIELDS: ClassVar[]
    __args__: ClassVar[List[Any]]
    # custom
    __eval_env__: bool = None

    __config_sections__: ClassVar[ConfigArgument]
    __config_files__: ClassVar[ConfigArgument]
    __ignored_slots__: ClassVar[List[str]]
    __multi_config__: ClassVar[bool]
    __config_list__: ClassVar[bool]
    __chain_files__: ClassVar[bool]
    __allow_empty_config__: ClassVar[bool]

    def __call__(self, *args, **kwargs) -> Union[DataclassProtocol, Any]:
        """Call Function."""
        ...

    def __config_filter_function__(self) -> bool:
        """Callback function to filter config."""
        ...

    def to_dict(self, *args, **kwargs) -> Any:
        """Parse config to dict.

        Method implemented in :meth:`cornflakes.decorator.dataclass._dataclass.to_dict`.
        """
        ...

    def to_tuple(self, *args, **kwargs) -> Any:
        """Parse config to tuple.

        Method implemented in :meth:`cornflakes.decorator.dataclass._dataclass.to_tuple`.
        """
        ...

    def to_ini(self, *args, **kwargs) -> Optional[bytearray]:
        """Parse config to ini file / bytes.

        Method implemented in :meth:`cornflakes.decorator.config.ini.to_ini`.
        """
        ...

    def to_yaml(self, *args, **kwargs) -> Optional[bytearray]:
        """Parse config to yaml file / bytes.

        Method implemented in :meth:`cornflakes.decorator.config.yaml.to_yaml`.
        """
        ...

    def to_yaml_bytes(self, *args, **kwargs) -> Optional[bytearray]:
        """Parse config to yaml bytes.

        Method implemented in :meth:`cornflakes.decorator.config.yaml.to_yaml_bytes`.
        """
        ...

    def to_ini_bytes(self, *args, **kwargs) -> Optional[bytearray]:
        """Parse config to ini bytes.

        Method implemented in :meth:`cornflakes.decorator.config.ini.to_ini_bytes`.
        """
        ...

    def validate_kwargs(self, validate=False, **kwargs) -> Dict[str, Any]:
        """Validate kwargs.

        Method implemented in :meth:`cornflakes.decorator.dataclass._validate.validate_dataclass_kwargs`.
        """
        ...

    def check_kwargs(self, validate=False, **kwargs) -> Dict[str, Any]:
        """Check dataclass kwargs.

        Method implemented in :meth:`cornflakes.decorator.dataclass._validate.check_dataclass_kwargs`.
        """
        ...

    from_ini: LoaderMethod
    from_yaml: LoaderMethod
    from_dict: LoaderMethod
    from_file: LoaderMethod


@runtime_checkable
class ConfigGroup(Protocol):
    """ConfigGroup Protocol Type."""

    # stdlib attributes
    __dataclass_fields__: ClassVar[Dict[str, Any]]
    __dataclass_params__: ClassVar[Dict]  # in reality `dataclasses._DataclassParams`
    __annotations__: ClassVar[Dict]
    __post_init__: ClassVar[Optional[Callable[..., None]]]
    # _FIELDS: ClassVar[]
    __args__: ClassVar[List[Any]]
    # custom
    __eval_env__: bool = None

    __config_files__: ClassVar[ConfigArgument]
    __multi_config__: ClassVar[bool]
    __config_list__: ClassVar[bool]
    __chain_files__: ClassVar[bool]
    __allow_empty_config__: ClassVar[bool]

    def __call__(self, *args, **kwargs) -> Union[DataclassProtocol, Any]:
        """Call Function."""
        ...

    def __config_filter_function__(self) -> bool:
        """Callback function to filter config."""
        ...

    def to_dict(self, *args, **kwargs) -> Any:
        """Parse config to dict.

        Method implemented in :meth:`cornflakes.decorator.dataclass._dataclass.to_dict`.
        """
        ...

    def to_tuple(self, *args, **kwargs) -> Any:
        """Parse config to tuple.

        Method implemented in :meth:`cornflakes.decorator.dataclass._dataclass.to_tuple`.
        """
        ...

    def to_ini(self, *args, **kwargs) -> Optional[bytearray]:
        """Parse config to ini file / bytes.

        Method implemented in :meth:`cornflakes.decorator.config.ini.to_ini`.
        """
        ...

    def to_yaml(self, *args, **kwargs) -> Optional[bytearray]:
        """Parse config to yaml file / bytes.

        Method implemented in :meth:`cornflakes.decorator.config.yaml.to_yaml`.
        """
        ...

    def to_yaml_bytes(self, *args, **kwargs) -> Optional[bytearray]:
        """Parse config to yaml bytes.

        Method implemented in :meth:`cornflakes.decorator.config.yaml.to_yaml_bytes`.
        """
        ...

    def to_ini_bytes(self, *args, **kwargs) -> Optional[bytearray]:
        """Parse config to ini bytes.

        Method implemented in :meth:`cornflakes.decorator.config.ini.to_ini_bytes`.
        """
        ...

    def validate_kwargs(self, validate=False, **kwargs) -> Dict[str, Any]:
        """Validate kwargs.

        Method implemented in :meth:`cornflakes.decorator.dataclass._validate.validate_dataclass_kwargs`.
        """
        ...

    def check_kwargs(self, validate=False, **kwargs) -> Dict[str, Any]:
        """Check dataclass kwargs.

        Method implemented in :meth:`cornflakes.decorator.dataclass._validate.check_dataclass_kwargs`.
        """
        ...

    from_ini: LoaderMethod
    from_yaml: LoaderMethod
    from_dict: LoaderMethod
    from_file: LoaderMethod
