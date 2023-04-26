from decimal import Decimal
from enum import Enum
import json


def type_to_str(f):
    """Function to convert python object to string -> fix scientific notation for float / Decimal."""
    if isinstance(f, Decimal) or isinstance(f, float):
        return (
            f"0.{'0' * (int(string[(e + 2):]) - 1)}{string[0]}{string[2:e]}"
            if (e := (string := str(f).lower()).find("e")) != -1
            else str(f)
        )
    if isinstance(f, bool):
        return str(f)
    if isinstance(f, int):
        return f
    if isinstance(f, Enum):
        return str(f.value)
    if isinstance(f, (list, tuple)):
        return json.dumps([v_str for v in f if (v_str := type_to_str(v))])
    if isinstance(f, dict):
        return json.dumps({k: type_to_str(v) for k, v in f.items()})
    return str(f or "")
