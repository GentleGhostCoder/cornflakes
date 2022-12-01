from functools import update_wrapper, wraps
import typing as t

from click import Command, get_current_context

F = t.TypeVar("F", bound=t.Callable[..., t.Any])
FC = t.TypeVar("FC", bound=t.Union[t.Callable[..., t.Any], Command])


def pass_context(f: F) -> F:
    """Marks a callback as wanting to receive the current context object as first argument."""

    @wraps(f)
    def new_func(*args, **kwargs):  # type: ignore
        return f(get_current_context(), *args, **kwargs)

    return update_wrapper(t.cast(F, new_func), f)
