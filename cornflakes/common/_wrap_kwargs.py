import dataclasses
from dataclasses import dataclass, field
from functools import wraps
import inspect
from inspect import Parameter, Signature, signature
from typing import Any, Callable, Dict, List, Optional

_HAS_DEFAULT_FACTORY = getattr(dataclasses, "_HAS_DEFAULT_FACTORY", None)
Empty = getattr(inspect, "_empty", None)


# from cornflakes.decorator.dataclass._dataclass import dataclass as data


def _not_excluded(default):
    return default != _HAS_DEFAULT_FACTORY


def _not_empty(x):
    return x != Empty


def _check_default(default):
    return _not_empty(default) and _not_excluded(default)


def _check_annotation(annotation):
    return _not_empty(annotation)


@dataclass
class KwargsWrapper:
    """KwargsWrapper Class."""

    wrapped_sig: Optional[Signature] = field(default=None, init=False)
    key_names: List[str] = field(default_factory=list, init=False)
    arg_names: List[str] = field(default_factory=list, init=False)
    kwarg_names: List[str] = field(default_factory=list, init=False)
    wrapped: Optional[Callable[..., Any]] = field(default=None)
    key_params: List[Parameter] = field(default_factory=list)
    key_params_no_default: List[Parameter] = field(default_factory=list)
    arg_params: List[Parameter] = field(default_factory=list)
    kwarg_params: List[Parameter] = field(default_factory=list)

    @property
    def _names(self):
        return [*self.key_names, *self.arg_names, *self.kwarg_names]

    @property
    def _passed_names(self):
        return ", ".join(
            [
                *[f"{key}={key}" for key in self.key_names],
                *[f"*{arg}" for arg in self.arg_names],
                *[f"**{arg}" for arg in self.kwarg_names],
            ]
        )

    @property
    def _params(self):
        return [*self.key_params_no_default, *self.arg_params, *self.key_params, *self.kwarg_params]

    @property
    def _params_declaration(self):
        return ", ".join(
            [
                (
                    f'{str(param).split(":", 1)[0].split("=", 1)[0]}'
                    f'{f": wrapped_type_{idx} " * _check_annotation(param.annotation)}'
                    f'{f"=wrapped_default_value_{idx}" * _check_default(param.default)}'
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
            if name not in self._names:
                if _check_default(param.default):
                    self.key_names.append(name)
                    self.key_params.append(param)
                    continue
                if param.kind == Parameter.VAR_POSITIONAL:
                    self.arg_names.append(name)
                    self.arg_params.append(param)
                    continue
                if param.kind == Parameter.VAR_KEYWORD:
                    self.kwarg_names.append(name)
                    self.kwarg_params.append(param)
                    continue
                if _not_excluded(param.default):
                    self.key_names.append(name)
                    self.key_params_no_default.append(param)
                continue

            is_variadic = Parameter.VAR_POSITIONAL or Parameter.VAR_KEYWORD
            param_idx = self._names.index(name)
            # print(f"overwrite {self.params[param_idx].name} at {param_idx} with {name} of {self.names}")
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
                default=param.default if _check_default(param.default) else self._params[param_idx].default,
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
        # print(ldict)
        # print(self.params_declaration)
        # print(self.passed_names)
        wrapper_str = f"""
def wrap_kwargs({self._params_declaration}):
    return wrapper({self._passed_names})
"""
        # print(wrapper_str)
        exec(  # noqa: S102
            wrapper_str,
            locals(),
            ldict,
        )
        return wraps(self.wrapped)(ldict["wrap_kwargs"])


def wrap_kwargs(wrapped) -> Callable[..., Any]:
    """Function Decorator that can update all passed arguments (that can be a variable) of function."""
    kwargs_wrapper = KwargsWrapper(wrapped)

    def wrapper(func):
        return kwargs_wrapper.wrap(func)

    return wrapper
