from dataclasses import dataclass, field
from inspect import Parameter, Signature, signature
import traceback
from typing import Any, Callable, Dict, List, Optional

from cornflakes.types import HAS_DEFAULT_FACTORY, INSPECT_EMPTY_TYPE, MISSING, WITHOUT_DEFAULT, WITHOUT_DEFAULT_TYPE


def _not_default_factory(default):
    return default != HAS_DEFAULT_FACTORY


def _not_empty(x):
    return x not in [INSPECT_EMPTY_TYPE, MISSING, WITHOUT_DEFAULT, WITHOUT_DEFAULT_TYPE]


def _check_default(default):
    return _not_empty(default) and _not_default_factory(default)


def _check_annotation(annotation):
    return _not_empty(annotation)


class WrappedValue:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return repr(self.value)


def _filter_not_wrapped_kwargs(kwargs):
    return {key: value for key, value in kwargs.items() if not isinstance(value, WrappedValue)}


@dataclass
class KwargsWrapper:
    """KwargsWrapper Class."""

    wrapped_sig: Optional[Signature] = field(default=None, init=False)
    key_names_no_default: List[str] = field(default_factory=list, init=False)
    key_names: List[str] = field(default_factory=list, init=False)
    arg_names: List[str] = field(default_factory=list, init=False)
    kwarg_names: List[str] = field(default_factory=list, init=False)
    wrapped: Callable[..., object]
    overwrites: Dict[str, Any] = field(default_factory=dict)
    excluded: List[str] = field(default_factory=list)
    key_params: List[Parameter] = field(default_factory=list)
    key_params_no_default: List[Parameter] = field(default_factory=list)
    arg_params: List[Parameter] = field(default_factory=list)
    kwarg_params: List[Parameter] = field(default_factory=list)

    @property
    def _names(self):
        return [*self.key_names_no_default, *self.key_names, *self.arg_names, *self.kwarg_names]

    @property
    def _kwargs_builder(self):
        return (
            "{"
            + ", ".join(
                [
                    *[f"'{key}': {key}" for key in self.key_names_no_default],
                    *[f"'{key}': {key}" for key in self.key_names],
                    *[f"**{arg}" for arg in self.kwarg_names],
                ]
            )
            + "}"
        )

    @property
    def _params(self):
        return [*self.key_params_no_default, *self.key_params, *self.arg_params, *self.kwarg_params]

    @property
    def _params_declaration(self):
        return ", ".join(
            [
                (
                    f'{str(param).split(":", 1)[0].split("=", 1)[0]}'
                    f'{f": wrapped_type_{idx}" * _check_annotation(param.annotation)}'
                    f'{f"=WrappedValue(wrapped_default_value_{idx})" * _check_default(param.default)}'
                )
                for idx, param in enumerate(self._params)
            ]
        )

    @property
    def _defaults_dict(self):
        return {
            f"wrapped_default_value_{idx}": param.default
            for idx, param in enumerate(self._params)
            if _check_default(param.default)
        }

    @property
    def _annotations_dict(self):
        return {
            f"wrapped_type_{idx}": param.annotation
            for idx, param in enumerate(self._params)
            if _check_annotation(param.annotation)
        }

    def _update_params(self, parameters):
        for name, param in parameters.items():
            # update params for existing index in self._names
            is_variadic = param.kind == Parameter.VAR_POSITIONAL or param.kind == Parameter.VAR_KEYWORD
            if name not in self._names:
                if name in self.excluded:
                    continue
                if _check_default(self.overwrites.get(param.name, INSPECT_EMPTY_TYPE)) and not is_variadic:
                    self.key_names.append(name)
                    self.key_params.append(
                        Parameter(
                            param.name,
                            kind=param.kind,
                            default=self.overwrites.get(name, MISSING),
                            annotation=param.annotation,
                        )
                    )
                    continue
                if _check_default(param.default) and not is_variadic:
                    self.key_names.append(name)
                    self.key_params.append(param)
                    continue
                if is_variadic and param.kind == Parameter.VAR_POSITIONAL and not self.arg_names:
                    self.arg_names.append(name)
                    self.arg_params.append(param)
                    continue
                if is_variadic and param.kind == Parameter.VAR_KEYWORD and not self.kwarg_names:
                    self.kwarg_names.append(name)
                    self.kwarg_params.append(param)
                    continue
                if not is_variadic and _not_default_factory(param.default):
                    self.key_names_no_default.append(name)
                    self.key_params_no_default.append(param)
                continue  # continue -> add new index to self._names

            param_idx = self._names.index(name)
            if is_variadic:
                self._params[param_idx] = Parameter(
                    param.name,
                    kind=param.kind,
                    annotation=param.annotation
                    if _check_annotation(param.annotation)
                    else self._params[param_idx].annotation,
                )
                continue
            self._params[param_idx] = Parameter(
                param.name,
                kind=param.kind,
                default=(param.default if _check_default(param.default) else self._params[param_idx].default),
                annotation=param.annotation
                if _check_annotation(param.annotation)
                else self._params[param_idx].annotation,
            )

    def __post_init__(self):
        """Initialize the Class."""
        self.wrapped_sig: Signature = signature(self.wrapped)
        self._update_params(self.wrapped_sig.parameters)

    def wrap(self, wrapper: Callable[..., Any]) -> Callable[..., Any]:
        """Method to return the declaration string."""
        wrapper_sig: Signature = signature(wrapper)
        self._update_params(wrapper_sig.parameters)
        ldict: Dict[str, Any] = {**self._defaults_dict, **self._annotations_dict}
        wrapper_str = f"""
def wrap_kwargs({self._params_declaration}):
    _wrapped_kwargs = {self._kwargs_builder}
    {f'''
    _wrapped_kwargs = {self._kwargs_builder}
    argument_names = list(_wrapped_kwargs.keys())
    argument_values = {self.arg_names[0]}[: len(argument_names)]
    _wrapped_kwargs.update(dict(zip(argument_names, argument_values)))
''' if self.arg_names else ''}
    _wrapped_kwargs = _filter_not_wrapped_kwargs(_wrapped_kwargs)
    return wrapper(**_wrapped_kwargs)
"""
        try:
            exec(  # noqa: S102
                wrapper_str,
                {**locals(), **globals()},
                ldict,
            )
        except Exception as exc:
            raise SyntaxError(
                f"Failed to wrap {self.wrapped} over {wrapper} by exec: {wrapper_str}\n{traceback.format_exc()}"
            ) from exc
        ldict["wrap_kwargs"].__qualname__ = wrapper.__qualname__
        ldict["wrap_kwargs"].__module__ = wrapper.__module__
        ldict["wrap_kwargs"].__name__ = wrapper.__name__
        ldict["wrap_kwargs"].__doc__ = wrapper.__doc__
        return ldict["wrap_kwargs"]


def wrap_kwargs(wrapped, exclude: Optional[List[str]] = None, **overwrites):
    """
    Function Decorator that can update all passed arguments (that can be a variable) of function.

    Args:
        wrapped (Callable): The original function to be wrapped.
        exclude (List[str], optional): A list of keys to exclude from wrapping.
        **overwrites: Keyword arguments that specify default values to overwrite.

    Returns:
        Callable: A function that wraps the original function.

    >>> @wrap_kwargs(wrapped=sum)
    ... def new_sum(**kwargs):
    ...     return kwargs
    >>> new_sum([1, 2, 3])  # Output would be 16 because 'start' is overwritten to 10
    {'iterable': [1, 2, 3]}
    """
    kwargs_wrapper = KwargsWrapper(wrapped=wrapped, overwrites=overwrites, excluded=exclude or [])

    def wrapper(func):
        return kwargs_wrapper.wrap(func)

    return wrapper
