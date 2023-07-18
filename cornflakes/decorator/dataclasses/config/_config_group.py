from typing import Callable, List, Optional, Type, Union, overload

from typing_extensions import dataclass_transform  # type: ignore

from cornflakes.decorator import Index, funcat
from cornflakes.decorator.dataclasses._dataclass import dataclass
from cornflakes.decorator.dataclasses._field import Field, field
from cornflakes.decorator.dataclasses.config._ini import to_ini
from cornflakes.decorator.dataclasses.config._load_config_group import create_group_loader
from cornflakes.decorator.dataclasses.config._yaml import to_yaml
from cornflakes.types import _T, ConfigGroup, Constants, CornflakesDataclass, Loader, Writer


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
    eval_env: bool = False,
    validate: bool = False,
    updatable: bool = False,
    files: Optional[Union[List[str], str]] = None,
    allow_empty: Optional[bool] = None,
    chain_files: Optional[bool] = False,
    filter_function: Optional[Callable[..., bool]] = None,
    **kwargs,
) -> Callable[[Type[_T]], Union[Type[_T], Type[CornflakesDataclass], Type[ConfigGroup]]]:
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
    eval_env: bool = False,
    validate: bool = False,
    updatable: bool = False,
    files: Optional[Union[str, List[str]]] = None,
    allow_empty: Optional[bool] = None,
    chain_files: Optional[bool] = False,
    filter_function: Optional[Callable[..., bool]] = None,
    **kwargs,
) -> Union[Type[_T], Type[CornflakesDataclass], Type[ConfigGroup]]:
    ...


@dataclass_transform(field_specifiers=(field, Field))
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
    eval_env: bool = False,
    validate: bool = False,
    updatable: bool = False,
    files: Optional[Union[str, List[str]]] = None,
    allow_empty: Optional[bool] = None,
    chain_files: Optional[bool] = False,
    filter_function: Optional[Callable[..., bool]] = None,
    **kwargs,
) -> Union[
    Callable[[Type[_T]], Union[Type[ConfigGroup], Type[CornflakesDataclass], Type[_T]]],
    Type[CornflakesDataclass],
    Type[ConfigGroup],
    Type[_T],
]:
    """Config decorator with a Subset of configs to parse Ini Files.

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
    :param chain_files: flag indicating whether to chain files in to single config.
    :param filter_function: Optional filter method for config
    :param kwargs: Additional args for custom dataclass. (dict_factory, eval_env. ...).

    :returns: wrapped class or the wrapper itself with the custom default arguments if the config class is not

    """
    files = files if isinstance(files, list) else [files] if files else []

    kwargs.pop("validate", None)  # no validation for group but all sub configs if provided

    def wrapper(w_cls: Type[_T]) -> Union[Type[ConfigGroup], Type[CornflakesDataclass], Type[_T]]:
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
            eval_env=eval_env,
            validate=validate,
            updatable=updatable,
            **kwargs,
        )(w_cls)

        setattr(config_group_cls, Constants.config_decorator.FILES, files)
        setattr(config_group_cls, Constants.config_decorator.CHAIN_FILES, chain_files)
        setattr(config_group_cls, Constants.config_decorator.ALLOW_EMPTY, allow_empty)
        setattr(config_group_cls, Constants.config_decorator.FILTER_FUNCTION, filter_function)

        setattr(
            config_group_cls,
            Loader.FILE.value,
            staticmethod(funcat(Index.reset, funcat_where="wrap")(create_group_loader(cls=config_group_cls))),
        )

        # Set Writer
        setattr(config_group_cls, Writer.INI.value, to_ini)
        setattr(config_group_cls, Writer.YAML.value, to_yaml)

        return config_group_cls

    return wrapper(cls) if cls else wrapper  # type: ignore
