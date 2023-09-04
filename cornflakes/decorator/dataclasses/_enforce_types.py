from typing import TypeVar, Type
from cornflakes.decorator import wrap_kwargs
from cornflakes.decorator.dataclasses._validate import validate_dataclass_kwargs

_T = TypeVar("_T")


def enforce_types(cls: Type[_T], dc_cls=None) -> Type[_T]:  # noqa: C901
    """Adds a simple decorator enforce_types that enables enforcing strict typing on a function or dataclass using annotations."""

    default_kwargs = validate_dataclass_kwargs(dc_cls=cls, force=False)  # pre validation

    def pre_init_wrapper(init):
        @wrap_kwargs(init, **default_kwargs)
        def wrapper(self, **kwargs):
            kwargs.update(validate_dataclass_kwargs(dc_cls=cls, **kwargs))
            return init(self, **kwargs)  # type: ignore

        return wrapper

    setattr(cls, "__init__", pre_init_wrapper(cls.__init__))

    return cls
