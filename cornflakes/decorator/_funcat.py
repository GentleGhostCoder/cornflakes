from typing import Literal


def funcat(func, *f_args, funcat_where: Literal["after", "before", "wrap"] = "after", **f_kwargs):
    """Prepend a functionality."""

    def decorator(original_func):
        def new_func(*args, **kwargs):
            if funcat_where == "wrap":
                func(*f_args, **f_kwargs)
                result = original_func(*args, **kwargs)
                func(*f_args, **f_kwargs)
                return result
            elif funcat_where == "before":
                func(*f_args, **f_kwargs)
                return original_func(*args, **kwargs)
            else:
                result = original_func(*args, **kwargs)
                func(*f_args, **f_kwargs)
                return result

        return new_func

    return decorator
