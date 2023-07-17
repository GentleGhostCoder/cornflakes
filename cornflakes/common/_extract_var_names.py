import inspect
from typing import Any, Callable


def extract_var_names(obj: Callable[..., Any]) -> dict:
    """Extract variables from class or function."""
    return {key: value.default for key, value in inspect.signature(obj).parameters.items()}
