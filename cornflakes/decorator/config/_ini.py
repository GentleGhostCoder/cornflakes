from typing import Union

from cornflakes import ini_load
from cornflakes.common import type_to_str
from cornflakes.decorator.config._load_config import create_file_loader
from cornflakes.decorator.config._write_config import write_config
from cornflakes.logging import logger


def to_ini_bytes(self, title: str = None) -> bytearray:  # TODO: implement more type_to_str feature -> date format etc.
    """Method to write an instance of the main config class of the module into a ini bytearray."""
    _ini_bytes = bytearray()
    if any([not hasattr(getattr(self, cfg), "to_ini_bytes") for cfg in self.__slots__]):
        _ini_bytes.extend(bytes(f"[{title}]\n", "utf-8"))
        _ini_bytes.extend(
            bytes("\n".join([f'{cfg}="{type_to_str(getattr(self, cfg))}"' for cfg in self.__slots__]), "utf-8")
        )
        _ini_bytes.extend(b"\n\n")
        return _ini_bytes

    for cfg_name in self.__slots__:
        cfg_value = getattr(self, cfg_name)
        if hasattr(cfg_value, "to_ini_bytes"):
            _ini_bytes.extend(cfg_value.to_ini_bytes(cfg_name))
        else:
            logger.warning(f"The Value {cfg_name} of {title} be in a child config class!")

    _ini_bytes.extend(b"\n")
    return _ini_bytes


def to_ini(self, out_cfg: str = None) -> Union[None, bytearray]:
    """Method to write an instance of the main config class of the module into an ini file."""
    return write_config(self.to_ini_bytes(self.__class__.__name__.lower()))


def create_ini_file_loader(
    cls=None,
    use_regex: bool = False,
):
    """Method to create file loader for ini files."""

    def from_ini(*args, **kwargs):
        return create_file_loader(cls=cls, use_regex=use_regex, loader=ini_load)(*args, **kwargs)

    return from_ini
