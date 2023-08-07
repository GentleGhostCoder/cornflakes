import ast
from functools import partial
import inspect


def get_method_definition(func):
    """
    This function returns the string representation of a given function. It supports both lambda functions
    and functions defined using `def`. It also supports `functools.partial` objects.

    Args:
        func (callable): A function or a `functools.partial` object.

    Returns:
        str: A string representation of the function or `functools.partial` object.

    Examples:
    >>> def original_function(x, y, z=3):
    ...     return x + y + z
    ...
    >>> p = partial(original_function, 1, z=5)
    >>> get_method_definition(p)  # doctest: +NORMALIZE_WHITESPACE
    'partial(original_function, 1, z=5)'

    # >>> l = lambda x, y, z: print(x, y, z)
    # >>> get_method_definition(l)
    # 'lambda x, y, z: print(x, y, z)'
    #
    # >>> method = partial(lambda x, y, z: print(x, y, z), x=1)
    # >>> get_method_definition(method)
    # 'partial(lambda x, y, z: print(x, y, z), x=1)'
    """
    if isinstance(func, partial):
        source_line = get_method_definition(func.func)
        pos_args = ", ".join(map(repr, func.args))
        kw_args = ", ".join(f"{k}={v!r}" for k, v in func.keywords.items())
        all_args = ", ".join(filter(bool, [pos_args, kw_args]))
        return f"partial({source_line}, {all_args})"
    return _extract_source_code(func)


def _extract_source_code(func):
    func_name = func.__name__
    if func_name != "<lambda>":
        return func_name

    sig = inspect.signature(func)
    params = str(sig)[1:-1]  # remove parentheses

    source_line = inspect.getsource(func)

    # Find the lambda keyword along with its specified parameters
    lambda_keyword = f"lambda {params}"
    lambda_index = source_line.find(lambda_keyword)
    if lambda_index != -1:
        if "partial" in source_line:
            lambda_index = source_line.find("partial")
        source_line = source_line[lambda_index:]

    tree = ast.parse(source_line.strip())
    for node in ast.walk(tree):
        if isinstance(node, ast.Lambda):
            return source_line[node.col_offset : node.end_col_offset].strip()
