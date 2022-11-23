from os import path
from typing import Optional, Union


def write_config(config_bytes: bytearray, out_cfg: Optional[str] = None) -> Union[bytearray, None]:
    """Method to write bytes into file."""
    if not out_cfg:
        return config_bytes
    with open(path.abspath(path.expanduser(out_cfg)), "wb") as f:
        f.write(config_bytes)
    return None
