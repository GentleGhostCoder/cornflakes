from cornflakes.decorator._wrap_kwargs import wrap_kwargs
from cornflakes.types import FuncatTypes


def funcat(func, *f_args, where: FuncatTypes = FuncatTypes.AFTER, **f_kwargs):
    """Prepend a functionality."""

    def decorator(original_func):
        @wrap_kwargs(original_func)
        def new_func(*args, **kwargs):
            if where == FuncatTypes.WRAP:
                func(*f_args, **f_kwargs)
                result = original_func(*args, **kwargs)
                func(*f_args, **f_kwargs)
                return result
            elif where == FuncatTypes.BEFORE:
                func(*f_args, **f_kwargs)
                return original_func(*args, **kwargs)
            else:
                result = original_func(*args, **kwargs)
                func(*f_args, **f_kwargs)
                return result

        return new_func

    return decorator
