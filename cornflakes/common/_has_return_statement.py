import ast
import inspect
import textwrap


def has_return_statement(func):
    source = inspect.getsource(func)
    source = textwrap.dedent(source)  # Remove leading whitespace
    tree = ast.parse(source)

    has_return = False
    all_returns_none = True  # Assume all returns are None until proven otherwise

    for node in ast.walk(tree):
        if isinstance(node, ast.Return):
            has_return = True  # Found a return statement
            if node.value is not None:  # Check if the return statement returns something other than None
                all_returns_none = False
                break  # No need to continue checking

    if not has_return:
        return False  # No return statement found

    if all_returns_none:
        return False  # All return statements are of type None

    return True  # There's at least one return statement that is not None
