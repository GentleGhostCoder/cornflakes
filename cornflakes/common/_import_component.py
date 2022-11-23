from functools import reduce
from typing import Any, List


def __get_or_call(module: Any, value: str) -> Any:
    if value[-2:] != "()":
        return getattr(module, value)
    return getattr(module, value[:-2])()


def import_component(key: str) -> Any:
    """Import object by key from inside ob module / submodule."""
    module = __import__(key)
    return reduce(__get_or_call, [module, *key.split(".")[1:]])


def __extract_code_varnames(module: Any) -> List[str]:
    if hasattr(module, "__code__"):
        return [k for k in module.__code__.co_varnames if k not in ["self", "kwargs", "args", "e"]]
    elif hasattr(module, "__init__"):
        return __extract_code_varnames(module.__init__)
    return []


def extract_var_names(key: str) -> List[str]:
    """Extract variables from class or function."""
    module = __import__(key.split(".", 1)[0])
    return __extract_code_varnames(reduce(__get_or_call, [module, *key.split(".")[1:]]))
