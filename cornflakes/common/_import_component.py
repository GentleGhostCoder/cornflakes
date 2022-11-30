from functools import reduce
import inspect
from typing import Any, Callable, Union


def __get_or_call(module: Any, value: str) -> Any:
    if value[-2:] != "()":
        return getattr(module, value)
    return getattr(module, value[:-2])()


def import_component(key: str) -> Any:
    """Import object by key from inside ob module / submodule."""
    module = __import__(key)
    return reduce(__get_or_call, [module, *key.split(".")[1:]])


def extract_var_names(obj: Union[str, Callable]) -> dict:
    """Extract variables from class or function."""
    return {key: value.default for key, value in inspect.signature(obj).parameters.items()}
