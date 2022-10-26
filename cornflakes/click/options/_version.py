from inspect import getfile
from typing import Callable, Union

from click import Command, Group, style
from click import version_option as click_version_option
import pkg_resources


def version_option(
    *args, **kwargs
) -> Callable[[Union[Command, Group, Callable[..., None]]], Union[Command, Group, Callable[..., None], Callable]]:
    """Click Option Decorator to define a global option for cli decorator."""
    _version = None
    _param_decls = []
    if args:
        _version = args[0]

    if len(args) > 1:
        _param_decls = args[1:]

    def global_option_decorator(option_func: Union[Union[Command, Group], Callable[..., None]]):
        if not callable(option_func):
            return option_func

        name = option_func.__qualname__
        module = getfile(option_func)
        version = _version or "0.0.1"

        if not _version and hasattr(option_func, "__module__"):
            module = option_func.__module__.split(".", 1)[0]
            if module != "__main__":
                version = pkg_resources.get_distribution(module).version

        version_args = {
            "prog_name": name,
            "version": args or version,
            "message": style(f"\033[95m{module}\033" f"[0m \033[95m" f"Version\033[0m: \033[1m" f"{version}\033[0m"),
        }

        version_args.update(kwargs)

        return click_version_option(*_param_decls, **version_args)(option_func)

    return global_option_decorator
