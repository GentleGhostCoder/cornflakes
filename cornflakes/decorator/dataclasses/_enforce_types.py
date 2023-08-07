from typing import TypeVar, Type

from cornflakes.decorator import wrap_kwargs
from cornflakes.decorator.dataclasses._validate import validate_dataclass_kwargs

_T = TypeVar("_T")


def enforce_types(cls: Type[_T], validate=False) -> Type[_T]:  # noqa: C901
    """Adds a simple decorator enforce_types that enables enforcing strict typing on a function or dataclass using annotations."""

    def pre_init_wrapper(init):
        @wrap_kwargs(init)
        def wrapper(*args, **kwargs):
            # argument_names = init.__code__.co_varnames[1:]
            # argument_values = args[: len(argument_names)]
            # kwargs.update(dict(zip(argument_names, argument_values)))  # noqa: B905
            # default_kwargs = {}
            # default_kwargs.update(kwargs)
            kwargs.update(validate_dataclass_kwargs(dc_cls=cls, validate=validate, **kwargs))
            return init(*args, **kwargs)  # type: ignore

        return wrapper

    setattr(cls, "__init__", pre_init_wrapper(cls.__init__))

    return cls
