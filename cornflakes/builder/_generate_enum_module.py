import re
from typing import Dict, List, Optional, Union


def generate_enum_module(source_dict: Union[str, List[str], Dict[str, str]], target_module_file: Optional[str]):
    """Generate Schema Types Enum from datahub module."""
    if isinstance(source_dict, list):
        enum = {re.sub(r"([a-z])([A-Z])", "\\1_\\2", key).replace(".", "_").upper(): key for key in source_dict}
    elif isinstance(source_dict, dict):
        enum = {
            re.sub(r"([a-z])([A-Z])", "\\1_\\2", key).replace(".", "_").upper(): value
            for key, value in source_dict.items()
        }
    else:
        raise ValueError(f"Unsupported type: {type(source_dict)}")

    enum = [f"{key} = {value!r}  # noqa: S105" for key, value in enum.items()]
    enum = """
    """.join(
        enum
    )
    with open(target_module_file, "w") as f:
        f.write(
            f'''"""Auto generated Schema Classes from datahub module."""
from enum import Enum


class SchemaTypes(str, Enum):
    """Schema Types."""
    {enum}
'''
        )
