from functools import wraps


def wraps_partial(*partial_args, **partial_kwargs):
    """Wraps a partial a function."""

    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            args = [*partial_args, *args[len(partial_args) :]]
            kwargs.update(partial_kwargs)
            return func(*args, **kwargs)

        return wrapper

    return decorate
