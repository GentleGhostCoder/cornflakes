from inspect import Parameter, signature
from typing import get_type_hints

from cornflakes.types import INSPECT_EMPTY_TYPE


def get_method_type_hint(method):
    """
    This function returns the type hint of a given function as a string in the format `Callable[[args], return]`.
    It supports functions with positional arguments, keyword arguments, variable positional arguments (`*args`),
    and variable keyword arguments (`**kwargs`). The type hints for `*args` and `**kwargs` are represented as `...`.

    Args:
        method (callable): A function.

    Returns:
        str: The type hint of the function as a string.

    Examples:
    >>> def func1(x: int, y: str) -> bool:
    ...     return y in str(x)
    ...
    >>> get_method_type_hint(func1)
    'Callable[[int, str], bool]'

    >>> def func2(x, y, *args, **kwargs):
    ...     return str(x) + y + str(args) + str(kwargs)
    ...
    >>> get_method_type_hint(func2)
    'Callable[..., Any]'

    >>> def func3(x, y):
    ...     return x + y
    ...
    >>> get_method_type_hint(func3)
    'Callable[[Any, Any], Any]'
    """
    sig = signature(method)

    if any(param.kind in [Parameter.VAR_POSITIONAL, Parameter.VAR_KEYWORD] for param in sig.parameters.values()):
        args_str = "..."
    else:
        args_str_list = []
        for param in sig.parameters.values():
            if param.annotation is INSPECT_EMPTY_TYPE:
                annotation = "Any"
            else:
                annotation = param.annotation.__name__
            args_str_list.append(str(annotation))
        args_str = ", ".join(args_str_list)

    type_hints = get_type_hints(method)
    if "return" in type_hints:
        return_str = str(type_hints["return"].__name__)
    else:
        return_str = "Any"

    return f"Callable[[{args_str}], {return_str}]"
