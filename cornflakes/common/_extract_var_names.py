import inspect
from typing import Callable, Union


def extract_var_names(obj: Union[str, Callable]) -> dict:
    """Extract variables from class or function."""
    return {key: value.default for key, value in inspect.signature(obj).parameters.items()}
