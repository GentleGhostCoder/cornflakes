from typing import Callable

from click import Option


def global_option(*option_args, **option_kwargs) -> Callable:
    """Click Option Decorator to define a global option for cli decorator."""
    _option = Option(*option_args, **option_kwargs)

    def global_option_decorator(option_func):
        if not callable(option_func):
            raise TypeError("Wrapped object should be a function!")

        if not hasattr(option_func, "params"):
            option_func.params = []

        option_func.params.append(_option)

        return option_func

    return global_option_decorator
