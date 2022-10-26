from typing import Union

from cornflakes import ini_load
from cornflakes.common import type_to_str
from cornflakes.decorator.config._load_config import create_file_loader
from cornflakes.decorator.config._load_config_group import create_group_loader
from cornflakes.decorator.config._write_config import write_config
from cornflakes.logging import logger


def _parse_config_list(cfg, cfg_name: str, title: str):
    _ini_bytes = bytearray()
    has_list = isinstance(cfg, list)
    is_config = hasattr(cfg, "__config_sections__")
    if is_config and not has_list:
        return cfg.to_ini_bytes(cfg_name)
    elif has_list:
        for n, sub_cfg in enumerate(cfg):
            _ini_bytes.extend(_parse_config_list(sub_cfg, f"{cfg_name}_{n}", title))
        return _ini_bytes
    else:
        logger.warning(f"The Value {cfg_name} of {title} be in a child config class!")
        return b""


def to_ini_bytes(self, title: str = None) -> bytearray:  # TODO: implement more type_to_str feature -> date format etc.
    """Method to write an instance of the main config class of the module into a ini bytearray."""
    _ini_bytes = bytearray()
    has_lists = isinstance(self, list)
    is_config = hasattr(self, "__config_sections__")
    if is_config and not has_lists:
        _ini_bytes.extend(bytes(f"[{title}]\n", "utf-8"))
        _ini_bytes.extend(
            bytes("\n".join([f'{cfg}="{type_to_str(getattr(self, cfg))}"' for cfg in self.__slots__]), "utf-8")
        )
        _ini_bytes.extend(b"\n\n")
        return _ini_bytes

    for cfg_name in self.__slots__:
        cfg = getattr(self, cfg_name)
        _ini_bytes.extend(_parse_config_list(cfg, cfg_name, title))

    _ini_bytes.pop()  # at least remove second line-break

    return _ini_bytes


def to_ini(self, out_cfg: str = None) -> Union[None, bytearray]:
    """Method to write an instance of the main config class of the module into an ini file."""
    return write_config(self.to_ini_bytes(self.__class__.__name__.lower()), out_cfg)


def create_ini_file_loader(
    cls=None,
):
    """Method to create file loader for ini files."""

    def from_ini(*args, **kwargs):
        return create_file_loader(cls=cls, loader=ini_load)(*args, **kwargs)

    return from_ini


def create_ini_group_loader(
    cls=None,
):
    """Method to create file loader for ini files."""

    def from_ini(*args, **kwargs):
        return create_group_loader(cls=cls, loader=ini_load)(*args, **kwargs)

    return from_ini
