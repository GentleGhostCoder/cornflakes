from contextlib import suppress
from functools import wraps
import inspect
from typing import Optional

SpecialForm = type(Optional)


def enforce_types(wrapped):
    """Adds a simple decorator enforce_types that enables enforcing strict typing on a function or dataclass using annotations.

    Works with collection types and subtypes for example Dict[str, Tuple[int, int]], and with special types as Optional and Any.
    Reference: https://github.com/matchawine/python-enforce-typing
    """
    spec = inspect.getfullargspec(wrapped)

    def check_types(*args, **kwargs):
        params = dict(zip(spec.args, args))
        params.update(kwargs)
        for name, value in params.items():
            with suppress(KeyError):
                type_hint = spec.annotations[name]
                if isinstance(type_hint, SpecialForm):
                    continue
                actual_type = getattr(type_hint, "__origin__", type_hint)
                actual_type = type_hint.__args__ if isinstance(actual_type, SpecialForm) else actual_type
                if not isinstance(value, actual_type):
                    raise TypeError(
                        f"Expected type '{type_hint}' for attribute '{name}' but received type '{type(value)}')"
                    )

    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            check_types(*args, **kwargs)
            return func(*args, **kwargs)

        return wrapper

    if inspect.isclass(wrapped):
        wrapped.__init__ = decorate(wrapped.__init__)
        return wrapped

    return decorate(wrapped)
