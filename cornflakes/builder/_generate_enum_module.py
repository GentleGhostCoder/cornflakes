import builtins
from importlib import import_module
from inspect import getmembers
import re
from types import ModuleType
from typing import Any, Dict, List, Optional, Union


def generate_enum_module(
    title: Optional[str],
    sources: Union[str, List[str], Dict[str, Any], ModuleType],
    target_module_file: Optional[str],
    module_description: Optional[str] = None,
    enum_description: Optional[str] = None,
    comments: Optional[Union[Dict[str, str], List[str]]] = None,
):
    """Generate Schema Types Enum from datahub module."""
    if isinstance(sources, list):
        enum = {re.sub(r"([a-z])([A-Z])", "\\1_\\2", key).replace(".", "_").upper(): f"{key!r}" for key in sources}
    elif isinstance(sources, dict):
        enum = {
            re.sub(r"([a-z])([A-Z])", "\\1_\\2", key).replace(".", "_").upper(): value for key, value in sources.items()
        }
    elif isinstance(sources, (ModuleType, str)):
        if isinstance(sources, str):
            sources = import_module(sources)
        enum = {
            re.sub(r"([a-z])([A-Z])", "\\1_\\2", key).replace(".", "_").upper(): f"{sources.__name__}.{key}"
            for key in getattr(sources, "__all__", [key for key, _ in getmembers(sources)])
            if (
                not key.startswith("_")
                and getattr(sources, key, None)
                and hasattr(getattr(sources, key, None), "__name__")
                and key not in dir(builtins)
            )
        }
    else:
        raise ValueError(f"Unsupported type: {type(sources)}")

    if comments:
        if isinstance(comments, list):
            for idx, comment in enumerate(comments):
                key = list(enum.keys())[idx]
                enum[key] = f"{enum[key]}  # {comment}"
        elif isinstance(comments, dict):
            for key, comment in comments.items():
                enum[key] = f"{enum[key]}  # {comment}"

    enum = [f"{key} = {value}" for key, value in enum.items()]
    enum = """
    """.join(
        enum
    )

    module_description = f'''"""{module_description}"""''' if module_description else ""  # noqa: B907
    enum_description = f'''"""{enum_description}"""''' if enum_description else ""  # noqa: B907

    module = f'''{f"""{module_description}
""" if module_description else ""}from enum import Enum
{f"""import {sources.__name__}
""" if not isinstance(sources, (list, dict)) else ""}

class {title}(Enum):
    {f"""{enum_description}
    """ if enum_description else ""}{enum}
'''

    with open(target_module_file, "w") as f:
        f.write(module)
