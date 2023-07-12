from typing import Union

from cornflakes.decorator._wrap_kwargs import wrap_kwargs
from cornflakes.decorator.types import Config, ConfigGroup, Dataclass


def enforce_types(dc_cls: Union[Dataclass, Config, ConfigGroup], validate=False):  # noqa: C901
    """Adds a simple decorator enforce_types that enables enforcing strict typing on a function or dataclass using annotations."""
    print(dc_cls)

    def decorate(func):
        @wrap_kwargs(func)
        def wrapper(self, *args, **kwargs):
            argument_names = func.__code__.co_varnames[1:]
            argument_values = args[: len(argument_names)]
            kwargs.update(dict(zip(argument_names, argument_values)))  # noqa: B905
            default_kwargs = {}
            default_kwargs.update(kwargs)
            default_kwargs.update(dc_cls.validate_kwargs(validate=validate, **default_kwargs))
            default_kwargs.pop("self", None)
            return func(self, **default_kwargs)  # type: ignore

        return wrapper

    dc_cls.__init__ = decorate(dc_cls.__init__)

    return dc_cls
