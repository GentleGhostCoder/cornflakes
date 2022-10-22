from os import path
from typing import Union


def write_config(bytes, out_cfg: str = None) -> Union[None, bytearray]:
    """Method to write bytes into file."""
    if not out_cfg:
        return bytes
    with open(path.abspath(path.expanduser(out_cfg)), "wb") as f:
        f.write(bytes)

    if not out_cfg:
        return bytes
    with open(path.abspath(path.expanduser(out_cfg)), "wb") as f:
        f.write(bytes)
