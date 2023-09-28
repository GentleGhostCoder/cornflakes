import logging
from typing import Any, Callable, List, Optional, Type, Union, overload

from typing_extensions import dataclass_transform  # type: ignore

from cornflakes.decorator._funcat import funcat
from cornflakes.decorator._indexer import Index
from cornflakes.decorator.dataclasses._config._config_group import config_group
from cornflakes.decorator.dataclasses._config._dict import create_dict_file_loader
from cornflakes.decorator.dataclasses._config._ini import create_ini_file_loader, to_ini
from cornflakes.decorator.dataclasses._config._init_config import wrap_init_default_config
from cornflakes.decorator.dataclasses._config._yaml import create_yaml_file_loader, to_yaml
from cornflakes.decorator.dataclasses._dataclass import dataclass
from cornflakes.decorator.dataclasses._field import Field, field
from cornflakes.decorator.dataclasses._helper import dataclass_fields, default, fields, get_default_loader
from cornflakes.decorator.dataclasses._validate import get_dataclass_non_comparable_kwargs
from cornflakes.types import (
    _T,
    Config,
    ConfigDecoratorArgs,
    ConfigGroup,
    Constants,
    CornflakesDataclass,
    FuncatTypes,
    Loader,
    MappingWrapper,
    Writer,
)

logger = logging.getLogger(__name__)


@dataclass_transform(field_specifiers=(field, Field))
@overload
def config(
    *,
    init: bool = True,
    repr: bool = True,
    eq: bool = True,
    order: bool = False,
    unsafe_hash: bool = False,
    frozen: bool = False,
    kw_only: bool = False,
    slots: bool = False,
    match_args: bool = True,
    dict_factory: Optional[Callable] = None,
    tuple_factory: Optional[Callable] = None,
    value_factory: Optional[Callable] = None,
    alias_generator: Optional[Callable[[str], str]] = None,
    eval_env: bool = False,
    validate: bool = False,
    updatable: bool = False,
    ignore_none: bool = False,
    files: Optional[Union[List[str], str]] = None,
    sections: Optional[Union[List[str], str]] = None,
    use_regex: Optional[bool] = False,
    is_list: Optional[Union[bool, int]] = False,
    default_loader: Optional[Loader] = None,
    allow_empty: Optional[bool] = False,
    chain_configs: Optional[bool] = False,
    **kwargs: Any,
) -> Callable[[Type[_T]], Union[Type[CornflakesDataclass], Type[Config], Type[ConfigGroup], MappingWrapper[_T]]]:
    ...


@dataclass_transform(field_specifiers=(field, Field))
@overload
def config(
    cls: Type[_T],
    /,
    *,
    init: bool = True,
    repr: bool = True,
    eq: bool = True,
    order: bool = False,
    unsafe_hash: bool = False,
    frozen: bool = False,
    kw_only: bool = False,
    slots: bool = False,
    match_args: bool = True,
    dict_factory: Optional[Callable] = None,
    tuple_factory: Optional[Callable] = None,
    value_factory: Optional[Callable] = None,
    alias_generator: Optional[Callable[[str], str]] = None,
    eval_env: bool = False,
    validate: bool = False,
    updatable: bool = False,
    ignore_none: bool = False,
    files: Optional[Union[List[str], str]] = None,
    sections: Optional[Union[List[str], str]] = None,
    use_regex: Optional[bool] = False,
    is_list: Optional[Union[bool, int]] = False,
    default_loader: Optional[Loader] = None,
    allow_empty: Optional[bool] = False,
    chain_configs: Optional[bool] = False,
    **kwargs: Any,
) -> Union[Type[Config], Type[CornflakesDataclass], Type[ConfigGroup], MappingWrapper[_T]]:
    ...


# @dataclass_transform(field_specifiers=(field, Field))
def config(
    cls: Optional[Type[_T]] = None,
    /,
    *,
    init: bool = True,
    repr: bool = True,
    eq: bool = True,
    order: bool = False,
    unsafe_hash: bool = False,
    frozen: bool = False,
    kw_only: bool = False,
    slots: bool = False,
    match_args: bool = True,
    dict_factory: Optional[Callable] = None,
    tuple_factory: Optional[Callable] = None,
    value_factory: Optional[Callable] = None,
    alias_generator: Optional[Callable[[str], str]] = None,
    eval_env: bool = False,
    validate: bool = False,
    updatable: bool = False,
    ignore_none: bool = False,
    files: Optional[Union[List[str], str]] = None,
    sections: Optional[Union[List[str], str]] = None,
    use_regex: Optional[bool] = False,
    is_list: Optional[Union[bool, int]] = False,
    default_loader: Optional[Loader] = None,
    allow_empty: Optional[bool] = False,
    chain_configs: Optional[bool] = False,
    init_default_config: Optional[bool] = True,
    **kwargs: Any,
) -> Union[
    Callable[[Type[_T]], Union[Type[Config], Type[CornflakesDataclass], Type[ConfigGroup], MappingWrapper[_T]]],
    Type[CornflakesDataclass],
    Type[Config],
    Type[ConfigGroup],
    MappingWrapper[_T],
]:
    """
    Config decorator to parse INI files and implement config loader methods to config-classes.

    :param alias_generator:
    :param ignore_none:
    :param value_factory:
    :param init_default_config:
    :param match_args:
    :param slots:
    :param kw_only:
    :param cls: The class type to create the config dataclass from.
    :type cls: class
    :param init: Whether to automatically add an __init__ method to the class. Default is True.
    :type init: bool, optional
    :param repr: Whether to automatically add a __repr__ method to the class. Default is True.
    :type repr: bool, optional
    :param eq: Whether to automatically add an __eq__ method to the class. Default is True.
    :type eq: bool, optional
    :param order: Whether to automatically add comparison methods (__lt__, __le__, __gt__, __ge__) to the class. Default is False.
    :type order: bool, optional
    :param unsafe_hash: Whether to add a __hash__ method to the class. Default is False.
    :type unsafe_hash: bool, optional
    :param frozen: Whether to make the generated class immutable. Default is False.
    :type frozen: bool, optional
    :param dict_factory: A function that returns a dict-like object which will be used as the base of the dataclass object. Default is None.
    :type dict_factory: Callable, optional
    :param tuple_factory: A function that returns a tuple-like object which will be used as the base of the dataclass object. Default is None.
    :type tuple_factory: Callable, optional
    :param eval_env: If set to True, will evaluate environment variables in the config file. Default is False.
    :type eval_env: bool, optional
    :param validate: If set to True, will validate the config file upon loading. Default is False.
    :type validate: bool, optional
    :param updatable: If set to True, the config object can be updated after it's created. Default is False.
    :type updatable: bool, optional
    :param files: A list or a single string of file path(s) to the default config files.
    :type files: Union[List[str], str], optional
    :param sections: A list or a single string of section name(s) in the config file(s).
    :type sections: Union[List[str], str], optional
    :param use_regex: If set to True, will evaluate all sections in the config file(s) by regex. Default is False.
    :type use_regex: bool, optional
    :param is_list: If set to True or a positive integer, will load the Config as a list of config class objects. Default is False.
    :type is_list: Union[bool, int], optional
    :param default_loader: The default config parser method.
    :type default_loader: Loader, optional
    :param allow_empty: If set to True, an empty config result will be allowed. Default is False.
    :type allow_empty: bool, optional
    :param chain_configs: If set to True, multiple config files will be chained into a single config. Default is False.
    :type chain_configs: bool, optional
    :param init_default_config: If set to True, will initialize the default config file(s) upon loading. Default is True.
    :type init_default_config: bool, optional

    :returns: If a class is given as `config_cls`, a new decorated class is returned. If no class is given, the decorator itself is returned with the custom default arguments.
    :rtype: Union[Type[Config], Type[ConfigGroup], Type[_T]], Callable[..., Union[Type[Config], Type[ConfigGroup], Type[_T]]]
    """
    sections = sections if isinstance(sections, list) else [sections] if sections else []
    files = files if isinstance(files, list) else [files] if files else []
    custom_loader: Optional[Callable] = None
    if not isinstance(default_loader, Loader) and callable(default_loader):
        custom_loader = default_loader
        default_loader = Loader.CUSTOM
    if not default_loader:
        default_loader = get_default_loader(files)

    def wrapper(
        w_cls: Type[_T],
    ) -> Union[Type[Config], Type[ConfigGroup], Type[CornflakesDataclass], MappingWrapper[_T]]:
        """Wrapper function for the config decorator config_decorator."""
        # Check __annotations__
        if not hasattr(w_cls, "__annotations__"):
            raise TypeError("The __annotations__ attribute is required in wrapped class")

        # Check is config
        if any(hasattr(slot, Constants.config_decorator.SECTIONS) for slot in w_cls.__annotations__.values()):
            logger.warning(
                "Wrapper config not working for a subset of config classes. "
                f"Please use {config_group.__name__} instead."
            )
            return config_group(
                files=files,
                init=init,
                repr=repr,
                eq=eq,
                order=order,
                unsafe_hash=unsafe_hash,
                frozen=frozen,
                kw_only=kw_only,
                slots=slots,
                match_args=match_args,
                dict_factory=dict_factory,
                tuple_factory=tuple_factory,
                value_factory=value_factory,
                eval_env=eval_env,
                validate=validate,
                updatable=updatable,
                ignore_none=ignore_none,
                **kwargs,
            )(w_cls)

        config_cls = dataclass(
            init=init,
            repr=repr,
            eq=eq,
            order=order,
            unsafe_hash=unsafe_hash,
            frozen=frozen,
            kw_only=kw_only,
            slots=slots,
            match_args=match_args,
            dict_factory=dict_factory,
            tuple_factory=tuple_factory,
            value_factory=value_factory,
            eval_env=eval_env,
            validate=validate,
            updatable=updatable,
            ignore_none=ignore_none,
            **kwargs,
        )(w_cls)

        # not allow field names that are in ConfigDecoratorArgs
        if any(f.name in dataclass_fields(ConfigDecoratorArgs) for f in fields(config_cls)):
            raise ValueError(f"Field name cannot be any of {dataclass_fields(ConfigDecoratorArgs).keys()}.")

        setattr(config_cls, Constants.config_decorator.SECTIONS, sections)
        setattr(config_cls, Constants.config_decorator.FILES, files)
        setattr(config_cls, Constants.config_decorator.USE_REGEX, use_regex)
        setattr(config_cls, Constants.config_decorator.IS_LIST, is_list)
        setattr(config_cls, Constants.config_decorator.chain_configs, chain_configs)
        setattr(config_cls, Constants.config_decorator.ALLOW_EMPTY, allow_empty)
        setattr(config_cls, Constants.config_decorator.VALIDATE, validate)
        setattr(config_cls, Constants.config_decorator.DEFAULT_LOADER, default_loader)
        setattr(config_cls, Constants.config_decorator.ALIAS_GENERATOR, alias_generator)

        setattr(
            config_cls,
            Constants.config_decorator.NON_COMPARABLE_FIELDS,
            get_dataclass_non_comparable_kwargs(
                {obj_name: default(obj) for obj_name, obj in dataclass_fields(config_cls).items()}
            ),
        )

        # Set Writer
        setattr(config_cls, Writer.INI.value, to_ini)
        setattr(config_cls, Writer.YAML.value, to_yaml)

        # Set Loader
        setattr(
            config_cls,
            Loader.YAML.value,
            staticmethod(create_yaml_file_loader(cls=config_cls)),
        )
        setattr(
            config_cls,
            Loader.INI.value,
            staticmethod(create_ini_file_loader(cls=config_cls)),
        )
        setattr(
            config_cls,
            Loader.DICT.value,
            staticmethod(create_dict_file_loader(cls=config_cls)),
        )

        if custom_loader:
            setattr(config_cls, Loader.CUSTOM.value, custom_loader)

        setattr(
            config_cls,
            Loader.FILE.value,
            getattr(config_cls, str(default_loader.value), getattr(config_cls, Loader.DICT.value)),
        )

        config_cls = wrap_init_default_config(config_cls, init_default_config=init_default_config)

        # check if any field type is type of Index and wrap Index reset over __init__
        if any(f.type == Index for f in fields(config_cls)):
            setattr(
                config_cls, "__init__", funcat(Index.reset, where=FuncatTypes.WRAP)(getattr(config_cls, "__init__"))
            )

        return config_cls

    return wrapper(cls) if cls else wrapper  # type: ignore
