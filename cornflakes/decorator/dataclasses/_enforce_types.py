from typing import TypeVar, Type

from cornflakes.decorator import wrap_kwargs
from cornflakes.decorator.dataclasses._validate import validate_dataclass_kwargs

_T = TypeVar("_T")


def enforce_types(cls: Type[_T], validate=False) -> Type[_T]:  # noqa: C901
    """Adds a simple decorator enforce_types that enables enforcing strict typing on a function or dataclass using annotations."""

    def decorate(func):
        @wrap_kwargs(func)
        def wrapper(self, *args, **kwargs):
            argument_names = func.__code__.co_varnames[1:]
            argument_values = args[: len(argument_names)]
            kwargs.update(dict(zip(argument_names, argument_values)))  # noqa: B905
            default_kwargs = {}
            default_kwargs.update(kwargs)
            default_kwargs.update(validate_dataclass_kwargs(dc_cls=cls, validate=validate, **default_kwargs))
            default_kwargs.pop("self", None)
            return func(self, **default_kwargs)  # type: ignore

        return wrapper

    setattr(cls, "__init__", decorate(cls.__init__))

    return cls
