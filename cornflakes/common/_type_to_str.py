from decimal import Decimal
from enum import Enum


def type_to_str(f):
    """Function to convert python object to string -> fix scientific notation for float / Decimal."""
    if isinstance(f, Decimal) or isinstance(f, float):
        return (
            f"0.{'0' * (int(string[(e + 2):]) - 1)}{string[0]}{string[2:e]}"
            if (e := (string := str(f).lower()).find("e")) != -1
            else str(f)
        )
    if isinstance(f, Enum):
        return str(f.value)
    return str(f)
