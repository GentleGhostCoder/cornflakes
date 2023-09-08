from typing import Callable, List, Optional, Type, Union, overload

from typing_extensions import dataclass_transform  # type: ignore

from cornflakes.decorator._funcat import funcat
from cornflakes.decorator._indexer import Index
from cornflakes.decorator.dataclasses._config._ini import to_ini
from cornflakes.decorator.dataclasses._config._init_config_group import wrap_init_config_group
from cornflakes.decorator.dataclasses._config._yaml import to_yaml
from cornflakes.decorator.dataclasses._dataclass import dataclass
from cornflakes.decorator.dataclasses._field import Field, field
from cornflakes.types import _T, ConfigGroup, Constants, CornflakesDataclass, FuncatTypes, MappingWrapper, Writer


@dataclass_transform(field_specifiers=(field, Field))
@overload
def config_group(
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
    allow_empty: Optional[bool] = None,
    chain_configs: Optional[bool] = False,
    **kwargs,
) -> Callable[[Type[_T]], Union[Type[ConfigGroup], Type[CornflakesDataclass], MappingWrapper[_T]]]:
    ...


@dataclass_transform(field_specifiers=(field, Field))
@overload
def config_group(
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
    files: Optional[Union[str, List[str]]] = None,
    allow_empty: Optional[bool] = None,
    chain_configs: Optional[bool] = False,
    **kwargs,
) -> Union[Type[ConfigGroup], Type[CornflakesDataclass], MappingWrapper[_T]]:
    ...


# @dataclass_transform(field_specifiers=(field, Field))  # TODO: Fix dataclass_transform -> breaking attribute completion in pycharm
def config_group(
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
    files: Optional[Union[str, List[str]]] = None,
    allow_empty: Optional[bool] = None,
    chain_configs: Optional[bool] = False,
    **kwargs,
) -> Union[
    Callable[[Type[_T]], Union[Type[ConfigGroup], Type[CornflakesDataclass], MappingWrapper[_T]]],
    Type[ConfigGroup],
    Type[CornflakesDataclass],
    MappingWrapper[_T],
]:
    """Config decorator with a Subset of configs to parse Ini Files.

    :param ignore_none:
    :param alias_generator:
    :param value_factory:
    :param updatable:
    :param validate:
    :param eval_env:
    :param tuple_factory:
    :param dict_factory:
    :param match_args:
    :param slots:
    :param kw_only:
    :param frozen:
    :param unsafe_hash:
    :param order:
    :param eq:
    :param repr:
    :param init:
    :param cls: Config class
    :param files: Default config files
    :param allow_empty: Flag that allows empty config result
    :param chain_configs: flag indicating whether to chain files in to single config.
    :param kwargs: Additional args for custom dataclass. (dict_factory, eval_env. ...).

    :returns: wrapped class or the wrapper itself with the custom default arguments if the config class is not

    """
    files = files if isinstance(files, list) else [files] if files else []

    kwargs.pop("validate", None)  # no validation for group but all sub configs if provided

    def wrapper(w_cls: Type[_T]) -> Union[Type[ConfigGroup], Type[CornflakesDataclass], MappingWrapper[_T]]:
        config_group_cls = dataclass(
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

        setattr(config_group_cls, Constants.config_decorator.FILES, files)
        setattr(config_group_cls, Constants.config_decorator.chain_configs, chain_configs)
        setattr(config_group_cls, Constants.config_decorator.ALLOW_EMPTY, allow_empty)
        setattr(config_group_cls, Constants.config_decorator.ALIAS_GENERATOR, alias_generator)

        config_group_cls = wrap_init_config_group(config_group_cls)

        # check if any field type is type of Index and wrap Index reset over __init__
        setattr(
            config_group_cls,
            "__init__",
            funcat(Index.group_indexing, where=FuncatTypes.WRAP)(getattr(config_group_cls, "__init__")),
        )

        # if any(f.type == Index for f in fields(config_group_cls)):
        #     setattr(config_group_cls, "__init__", funcat(Index.reset(), where=FuncatTypes.WRAP)(config_group_cls.__init__))

        # Set Writer
        setattr(config_group_cls, Writer.INI.value, to_ini)
        setattr(config_group_cls, Writer.YAML.value, to_yaml)

        return config_group_cls

    return wrapper(cls) if cls else wrapper  # type: ignore
