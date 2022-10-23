from typing import Callable, Union

from click import Command, Group, Option


def global_option(
    *option_args, **option_kwargs
) -> Callable[[Union[Command, Group, Callable[..., None]]], Union[Command, Group, Callable[..., None], Callable]]:
    """Click Option Decorator to define a global option for cli decorator."""
    _option = Option(*option_args, **option_kwargs)

    def global_option_decorator(option_func: Union[Union[Command, Group], Callable[..., None]]):
        if not callable(option_func):
            return option_func

        if not hasattr(option_func, "params"):
            option_func.params = []
        option_func.params.append(_option)

        return option_func

    return global_option_decorator
