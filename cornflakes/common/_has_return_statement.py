import ast
import inspect
import textwrap


def has_return_statement(func):
    source = inspect.getsource(func)
    source = textwrap.dedent(source)  # Remove leading whitespace
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.Return):
            return True
    return False
