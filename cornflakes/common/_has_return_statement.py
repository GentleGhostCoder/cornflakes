import dis


def has_return_statement(func):
    """
    Checks if a given function has a return statement that returns a value other than None.

    :param func: The function to be checked
    :type func: Callable
    :return: True if the function has a return statement that returns a value other than None, False otherwise.
    :rtype: bool

    :xdoctest:

    >>> def no_return(): pass
    >>> has_return_statement(no_return)
    False

    >>> def return_none():
    ...     return None
    >>> has_return_statement(return_none)
    False

    >>> def return_something():
    ...     return 42
    >>> has_return_statement(return_something)
    True

    >>> def return_conditionally(x):
    ...     if x > 0:
    ...         return x
    >>> has_return_statement(return_conditionally)
    True

    >>> def multiple_return(x):
    ...     if x > 0:
    ...         return None
    ...     return x
    >>> has_return_statement(multiple_return)
    True

    >>> def multiple_none_return(x):
    ...     if x > 0:
    ...         return None
    ...     return None
    >>> has_return_statement(multiple_none_return)
    False
    """

    return_count = 0
    none_return_count = 0
    has_load_const_none = False

    for inst in dis.get_instructions(func):
        if inst.opname == "LOAD_CONST" and inst.argval is None:
            has_load_const_none = True
        if inst.opname == "RETURN_VALUE":
            return_count += 1
            if has_load_const_none:
                none_return_count += 1
            has_load_const_none = False

    return return_count > none_return_count
