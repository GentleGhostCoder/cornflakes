from enum import Enum
import re
from typing import Dict, Optional, Union


def generate_enum_module_from_dict(source_dict: Union[str, Dict[str, str]], target_module_file: Optional[str]):
    """Generate Schema Types Enum from datahub module."""
    enum = Enum(
        "SchemaTypes",
        {key.replace(".", "_"): value for key, value in source_dict.items()},
    )
    enum = {re.sub(r"([a-z])([A-Z])", "\\1_\\2", enum.value.__name__).upper(): enum.value.__name__ for enum in enum}
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
