"""Module for checking types of variables.

The `check_type` function provides a mechanism to check if a given value matches the specified type hint.
Works with collection types and subtypes for example Dict[str, Tuple[int, int]], and with special types as Optional and Any.
Base Reference: https://github.com/matchawine/python-enforce-typing
"""
from dataclasses import is_dataclass
import inspect
from itertools import chain
from typing import Any, Optional, get_args

SpecialForm = type(Optional)
AnyMeta = type(Any)


def check_type(type_hint: Any, value, key="", skip=False):
    """
    Check if the provided value matches the specified type hint.

    :param type_hint: The type hint or annotation to check against.
    :param key: The attribute or variable name. (only required for error messages)
    :param value: The value to be checked.
    :param skip: If True, skip the type check and return None. Defaults to False.
    :return: The value if it matches the type hint.
    :raises TypeError: If the value does not match the expected type.
    :raises ValueError: If an error occurs during type conversion or when the value does not match the expected type.

    This function handles various scenarios, including handling of special types, class types, dataclasses,
    unions, lists, tuples, built-in types, and custom types.

    Example:
    ```
    # Checking if a value matches the type hint
    result = check_type(int, 'my_var', 10)
    # `result` will be 10, as it matches the `int` type hint.
    ```
    """
    # If the type hint is None or a special form (like Optional), we return the value as is.
    if isinstance(type_hint, (type(None), SpecialForm, AnyMeta)):
        return value

    # If the type hint is a class and the value is an instance of that class, we return the value as is.
    if inspect.isclass(type_hint) and isinstance(value, type_hint):
        return value

    # If the type hint is a dataclass and the value is a dictionary, we instantiate the dataclass with the dictionary values and return the result.
    if is_dataclass(type_hint) and isinstance(value, dict):
        return type_hint(**value)

    # We get the actual type of the type hint. This handles cases where the type hint is a more complex form, like a Union or a List.
    actual_type: Any = get_actual_type(type_hint)

    # If the actual type is a string, we convert the value to a string and return it.
    if actual_type == str:
        return str(value or "")

    # If the actual type is a list or tuple, we check each element of the value against the corresponding type in the type hint.
    if isinstance(actual_type, (list, tuple)):
        return _check_list_or_tuple_type(actual_type, key, value, skip)

    # If the actual type is the list or tuple type itself, we check that the value is a list or tuple.
    if actual_type in [list, tuple]:
        return _check_list_or_tuple(actual_type, type_hint, key, value, skip)

    # If the actual type is a built-in function or a user-defined function, we call the function with the value as argument and return the result.
    if inspect.isbuiltin(actual_type) or inspect.isfunction(actual_type):
        return actual_type(value)

    # If the actual type is a class, we check that the value is an instance of that class.
    return _check_class_type(actual_type, type_hint, key, value, skip)


def get_actual_type(type_hint):
    """Returns the actual type of the type hint."""
    actual_type = getattr(type_hint, "__origin__", getattr(type_hint, "type", type_hint))
    if isinstance(actual_type, SpecialForm):
        actual_type = getattr(type_hint, "__args__", type_hint)
    return (
        actual_type
        if inspect.isclass(type_hint) or isinstance(type_hint, (list, tuple))
        else get_actual_type(actual_type)
    )


def _check_list_or_tuple_type(actual_type, key, value, skip):
    actual_types = (
        [t for t in actual_type if t is not None]
        if value
        else [type(None)]
        if type(None) in actual_type
        else actual_type
    )
    if not any(inspect.isclass(t) for t in actual_types):
        if value not in actual_types:
            if skip:
                return
            raise TypeError(
                f"Expected any of {actual_types!r} for attribute {key!r} but received type {type(value)!r})."
            )
        actual_types = [type(t) for t in actual_types]
    values = [check_type(t, value, key, skip=True) for t in actual_types]
    if not any(values) and type(None) in actual_types:
        return None
    if not any(values):
        if skip:
            return
        raise TypeError(f"Expected any of {actual_types!r} for attribute {key!r} but received type {type(value)!r}).")
    return next(item for item in values if item is not None)


def _check_list_or_tuple(actual_type, type_hint, key, value, skip):
    if not isinstance(value, (list, tuple)):
        if skip:
            return
        raise TypeError(f"Expected type {type_hint!r} for attribute {key!r} but received type {type(value)!r}).")
    actual_types = [t for t in get_args(type_hint) if t is not None] or [str] if value else [type(None)]
    if len(value) > len(actual_types):
        actual_types = [actual_types[0]] * len(value) if len(actual_types) else [type(None)] * len(value)
    return actual_type(chain([check_type(t, val, key) for val, t in zip(value, actual_types)]))


def _check_class_type(actual_type, type_hint, key, value, skip):
    if not isinstance(value, actual_type):
        try:
            return actual_type(value)  # type: ignore
        except Exception as exc:
            if skip:
                return
            raise ValueError(
                f"\n{exc}\n" f"Expected type {actual_type!r} for attribute {key!r} but received type {type(value)!r})."
            ) from exc

    return value
