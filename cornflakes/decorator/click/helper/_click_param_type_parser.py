from dataclasses import is_dataclass
from functools import partial
from inspect import isclass

from click import Choice, ParamType

from cornflakes import eval_type
from cornflakes.common import get_actual_type
from cornflakes.decorator.dataclasses import check_dataclass_kwargs
from cornflakes.types import HIDDEN_DEFAULT_TYPE, MISSING_TYPE, WITHOUT_DEFAULT_TYPE


def click_param_type_parser(config):
    """Create click param type parser."""

    def create_click_param_type(type_class):
        if not isclass(type_class):
            type_class = get_actual_type(type_class)

        if isinstance(type_class, (list, tuple)):
            if all(isinstance(t, str) for t in type_class):
                return partial(lambda choices: Choice(choices), choices=type_class)
            type_class_name = "|".join(
                getattr(t, "__name__", str(t)) for t in type_class if t is not type(None)  # noqa: E721
            )
        elif is_dataclass(type_class):
            type_class_name = f"{type_class.__name__}(**DICT)"
        else:
            type_class_name = type_class.__name__

        class ClickParamType(ParamType):
            name = type_class_name

            def convert(self, value, param, ctx):
                if isinstance(value, HIDDEN_DEFAULT_TYPE):
                    return value
                if not isinstance(value, (MISSING_TYPE, WITHOUT_DEFAULT_TYPE)):
                    if isinstance(value, str):
                        value = eval_type(value)
                    return check_dataclass_kwargs(config, **{param.name: value})[param.name]

        return ClickParamType

    return create_click_param_type
