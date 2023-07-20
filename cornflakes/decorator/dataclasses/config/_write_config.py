from os import path
from typing import Optional


def write_config(config_bytes: bytearray, out_cfg: Optional[str] = None) -> Optional[bytearray]:
    """Method to write bytes into file."""
    if not out_cfg:
        return config_bytes
    with open(path.abspath(path.expanduser(out_cfg)), "wb") as f:
        f.write(config_bytes)
    return None
