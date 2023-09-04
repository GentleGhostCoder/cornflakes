import builtins
from dataclasses import InitVar
from importlib import import_module
from inspect import getmembers
import os
import re
import sysconfig
from types import ModuleType
from typing import Any, Dict, List, Optional, Type, Union

from cornflakes.common import get_method_definition, get_method_type_hint, recursive_update
from cornflakes.decorator import field, wrap_kwargs
from cornflakes.decorator.dataclasses import config
from cornflakes.decorator.dataclasses import dataclass as data


@data(slots=True)  # type: ignore
class _ConfigModuleGenerator:
    title: str
    target_module_file: str
    sources: InitVar[Union[str, List[str], Dict[str, Any], ModuleType]]
    to_upper: InitVar[bool]
    inherit_from: InitVar[Optional[List[Type[Any]]]] = None
    comments: InitVar[Optional[Union[Dict[str, str], List[str]]]] = None
    module_description: Optional[str] = None
    class_description: Optional[str] = None
    config_dict: Dict[str, Any] = field(default_factory=dict, init=False)
    imports: Optional[Dict[str, List[str]]] = field(default_factory=dict, init=False)
    types: Optional[List[str]] = field(default_factory=list, init=False)
    inherit_str: Optional[str] = ""

    def __post_init__(self, sources, comments, to_upper, inherit_from):
        self._handle_sources(sources)

        if comments:
            self._handle_comments(comments)

        # If 'to_upper' is True, convert all keys to uppercase.
        if to_upper:
            self.config_dict = {key.upper(): value for key, value in self.config_dict.items()}

        # Add all imports from the inherit_from list to the import_str string (if not builtins).
        if inherit_from:
            self.imports = {cls.__module__: cls.__name__ for cls in inherit_from if cls.__module__ != "builtins"}

        # Create a list of strings representing the config members.
        self._set_types([type(value).__name__ for value in self.config_dict.values()])

        # add all types to the key of the config dict.
        self.config_dict = {
            f"{key}: {_type}": value
            for key, value, _type in zip(self.config_dict.keys(), self.config_dict.values(), self.types)
        }

        # create the inherit_str string from the inherit_from list. -> (...) if inherit_from else ""
        self.inherit_str = f"({', '.join(cls.__name__ for cls in inherit_from)})" if inherit_from else ""

    def write_module(self, *args, **kwargs):
        imports_str = "\n".join(f"from {module} import {', '.join(cls)}" for module, cls in self.imports.items())
        config_list = [f"{key} = {value}" for key, value in self.config_dict.items()]
        # Join the list into a single string, with members separated by newlines.
        config_str = "\n    ".join(config_list)
        # Format the module and class descriptions.
        module_description = f'''"""{self.module_description}"""''' if self.module_description else ""  # noqa: B907
        class_description = f'''"""{self.class_description}"""''' if self.class_description else ""  # noqa: B907

        # Create config_args from the *args and **kwargs parameters. passed to the @config decorator.
        config_args = (
            f'({", ".join([f"{arg!r}" for arg in args] + [f"{key}={value!r}" for key, value in kwargs.items()])})'
            if args or kwargs
            else ""
        )

        # Format the entire module as a string.
        module = f'''{f"""{module_description}
""" if module_description else ""}from {import_module("cornflakes.decorator.dataclasses").__name__} import config
{imports_str}

@{config.__name__}{config_args}
class {self.title}{self.inherit_str}:
    {f"""{class_description}
    """ if class_description else ""}{config_str}
'''

        # Write the module string to the target file.
        with open(self.target_module_file, "w") as f:
            f.write(module)

        if os.path.exists(sysconfig.get_paths()["purelib"]):
            if "black" in os.listdir(sysconfig.get_paths()["purelib"]):
                # fix format
                # source_config = " ".join(source_config) if isinstance(source_config, list) else source_config
                os.system(f"black {self.target_module_file}")  # noqa: S605
            if "isort" in os.listdir(sysconfig.get_paths()["purelib"]):
                os.system(f"isort {self.target_module_file}")  # noqa: S605

    def _fix_iterable_types(self, types: list, actual_iter_type: str, typing_iter_type: str):
        recursive_update(self.imports, {"typing": [typing_iter_type]}, merge_lists=True)
        for idx, key in enumerate(types):
            if key == actual_iter_type and len(iter_value := list(self.config_dict.values())[idx]) > 0:
                if len(iter_value) > 1:
                    sub_types = self._fix_types([type(value).__name__ for value in iter_value])
                    # check if sub_types are unique
                    if len(set(sub_types)) == 1:
                        types[idx] = f"{typing_iter_type}[{sub_types[0]}]"
                    else:
                        # make Union and add to imports
                        recursive_update(self.imports, {"typing": ["Union"]}, merge_lists=True)
                        types[idx] = f"{typing_iter_type}[Union[{', '.join(sub_types)}]]"
                else:
                    types[idx] = f"{typing_iter_type}[{self._fix_types([type(iter_value[0]).__name__])[0][0]}]"
        return types

    def _fix_mapping_types(self, types: list, actual_mapping_type: str, typing_mapping_type: str):
        """Fix mapping types and add import to import_str"""
        recursive_update(self.imports, {"typing": [typing_mapping_type]}, merge_lists=True)
        for idx, key in enumerate(types):
            if (
                key == actual_mapping_type
                and len(mapping_values := list(list(self.config_dict.values())[idx].values())) > 0
            ):
                types[
                    idx
                ] = f"{typing_mapping_type}[{self._fix_types([type(mapping_values[0]).__name__])[0][0]}, {self._fix_types([type(mapping_values[1]).__name__])[0][0]}]"
        return types

    def _fix_function_types(self, types: list):
        # recursive_update(self.imports, {"typing": ["Callable"]}, merge_lists=True)
        for idx, key in enumerate(types):
            if key == "function" and callable(method := list(self.config_dict.values())[idx]):
                types[idx] = get_method_type_hint(method)
                self.config_dict[list(self.config_dict.keys())[idx]] = get_method_definition(method)
                # if not a lambda function, add the function module to the import str
                if not isinstance(method, type(lambda: None)) and not isinstance(
                    method, type(lambda: None).__bases__[0]
                ):
                    recursive_update(self.imports, {method.__module__: [method.__name__]}, merge_lists=True)
        return types

    def _set_types(self, types):
        # change all str to quoted str
        if "str" in types:
            self.config_dict = {
                key: f"{value!r}" if isinstance(value, str) else value for key, value in self.config_dict.items()
            }

        # any non builtin types thats value is of type module or class should be added to the import str and the type changed to Any
        for idx, key in enumerate(types):
            if key not in dir(builtins) and isinstance(
                value := list(self.config_dict.values())[idx], (ModuleType, type)
            ):
                recursive_update(self.imports, {value.__module__: [value.__name__]}, merge_lists=True)
                types[idx] = "Any"

        # any non builtin types thats value is a instance of a class should be added to the import str and the type changed to the instance class name and the value represented as the callable instantiation with the arguments (if the class has a __call__ / __init__ method)
        for idx, key in enumerate(types):
            value = list(self.config_dict.values())[idx]
            if key not in dir(builtins) and isinstance(value, type) and callable(value):
                recursive_update(self.imports, {value.__module__: [value.__name__]}, merge_lists=True)
                types[idx] = value.__name__
                self.config_dict[list(self.config_dict.keys())[idx]] = f"{value.__name__}()"
        self.types = self._fix_types(types)

    def _fix_types(self, types: list):
        # if the type is a list, fix all types n and add List[..fixed_type..] to import str
        if "list" in types:
            types = self._fix_iterable_types(types, "list", "List")

        if "tuple" in types:
            types = self._fix_iterable_types(types, "tuple", "Tuple")

        if "set" in types:
            types = self._fix_iterable_types(types, "set", "Set")

        if "dict" in types:
            types = self._fix_mapping_types(types, "dict", "Dict")

        # replace NoneType with Optional[Any] and add Optional + Any to import str
        if "NoneType" in types:
            recursive_update(self.imports, {"typing": ["Optional", "Any"]}, merge_lists=True)
            types = [type_.replace("NoneType", "Optional[Any]") for type_ in types]

        # replace function with Callable and add Callable to import str
        if "function" in types:
            recursive_update(self.imports, {"typing": ["Callable"]}, merge_lists=True)
            types = self._fix_function_types(types)

        return types

    def _handle_comments(self, comments):
        # If 'comments' is provided, add them to the 'config' dict.
        if isinstance(comments, list):
            # If 'comments' is a list, match comments with config members by index.
            for idx, comment in enumerate(comments):
                key = list(self.config_dict.keys())[idx]
                self.config_dict[key] = f"{self.config_dict[key]}  # {comment}"
        elif isinstance(comments, dict):
            # If 'comments' is a dict, match comments with config members by key.
            for key, comment in comments.items():
                self.config_dict[key] = f"{self.config_dict[key]}  # {comment}"

    def _handle_sources(self, sources):
        # Handle different types of 'sources'.
        if isinstance(sources, list):
            # If 'sources' is a list, create a dict where keys are the 'sources' elements formatted as uppercase strings
            # with underscores instead of dots, and values are the 'sources' elements as repr strings.
            self.config_dict = {
                re.sub(r"([a-z])([A-Z])", "\\1_\\2", key).replace(".", "_").upper(): f"{key!r}" for key in sources
            }
        elif isinstance(sources, dict):
            # If 'sources' is a dict, create a similar dict, but with values taken from the 'sources' dict.
            self.config_dict = {
                re.sub(r"([a-z])([A-Z])", "\\1_\\2", key).replace(".", "_"): value for key, value in sources.items()
            }
        elif isinstance(sources, (ModuleType, str)):
            # If 'sources' is a ModuleType or a str (assumed to be a module name), create a dict where keys are the names
            # of the items in the module (formatted as above), and values are the fully qualified names of the items.
            # Only items that are not built-in, do not start with an underscore, and have a '__name__' attribute are included.
            if isinstance(sources, str):
                sources = import_module(sources)
            self.config_dict = {
                re.sub(r"([a-z])([A-Z])", "\\1_\\2", key).replace(".", "_"): f"{sources.__name__}.{key}"
                for key in getattr(sources, "__all__", [key for key, _ in getmembers(sources)])
                if (
                    not key.startswith("_")
                    and getattr(sources, key, None)
                    and hasattr(getattr(sources, key, None), "__name__")
                    and key not in dir(builtins)
                )
            }
        else:
            # Raise an error if 'sources' is none of the supported types.
            raise ValueError(f"Unsupported type: {type(sources)}")


@wrap_kwargs(config)
def generate_config_module(
    title: str,
    sources: Union[str, List[str], Dict[str, Any], ModuleType],
    target_module_file: str,
    module_description: Optional[str] = None,
    class_description: Optional[str] = None,
    inherit_from: Optional[List[Type[Any]]] = None,
    comments: Optional[Union[Dict[str, str], List[str]]] = None,
    to_upper: bool = False,
    *args,
    **kwargs,
):
    """
    Generate a Python module with a single Config class from the provided sources.

     :param title: The name of the config class to be generated.
     :type title: Optional[str]
     :param sources: The source data from which to generate the config. Can be a list, dict, module, or the name of a module as a string.
     :type sources: Union[str, List[str], Dict[str, Any], ModuleType]
     :param target_module_file: The path to the file where the generated module will be written.
     :type target_module_file: str
     :param module_description: Description of the module to be included at the top of the generated file.
     :type module_description: Optional[str]
     :param class_description: Description of the config class to be included in the generated file.
     :type class_description: Optional[str]
     :param comments: Optional comments to be included next to each config member. Can be a list (in which case comments are matched with members by index) or a dict (in which case comments are matched with members by key).
     :type comments: Optional[Union[Dict[str, str], List[str]]]
     :param inherit_from: Optional list of classes to inherit from.
     :type inherit_from: Optional[List[Type[Any]]]
     :param to_upper: If True, convert all config members to uppercase.
     :type to_upper: bool
     :param args: Additional arguments to be passed to the @config decorator.
     :type args: Any
     :param kwargs: Additional keyword arguments to be passed to the @config decorator.
     :type kwargs: Any
     :raises ValueError: If the type of the 'sources' parameter is not supported.

    """
    # Handle different types of 'sources'.
    _ConfigModuleGenerator(
        sources=sources,
        comments=comments,
        to_upper=to_upper,
        inherit_from=inherit_from or [],
        title=title,
        target_module_file=target_module_file,
        module_description=module_description,
        class_description=class_description,
    ).write_module(*args, **kwargs)


# import selectors
#
# config_dict = {
#     # 'default_offset_commit_callback': lambda offsets, response: True,
#     # 'socket_options': [(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)],
#     "selector": selectors.DefaultSelector,
# }
# generate_config_module(
#     "KafkaConsumerConfig",
#     config_dict,
#     target_module_file="test_config_module.py",
#     module_description="Auto generated KafkaConsumerConfig Class from kafka module.",
#     class_description="KafkaConsumerConfig class for kafka module.",
#     frozen=True,
# )


# import inspect
# import opcode
#
# def get_creation_info(instance):
#     # Get the current frame
#     current_frame = inspect.currentframe()
#     # Go back to the frame where the instance was created
#     creation_frame = current_frame.f_back
#     # Get the file name and line number
#     creation_file = creation_frame.f_code.co_filename
#     creation_line = creation_frame.f_lineno
#     # Read the line from the file
#     with open(creation_file, 'r') as file:
#         lines = file.readlines()
#     creation_code = lines[creation_line - 1].strip()  # Subtract 1 because line numbers start at 1, but list indices start at 0
#     return f"Created at line {creation_line} in {creation_file}: {creation_code}"
#
# # Create an instance
# test_instance = decimal.Decimal("123")
#
# # Get the creation info
# print(get_creation_info(test_instance))
