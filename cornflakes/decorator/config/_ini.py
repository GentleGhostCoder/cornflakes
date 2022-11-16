import logging
from typing import Callable, Dict, List, Optional, Union

from cornflakes import ini_load
from cornflakes.common import type_to_str
from cornflakes.decorator.config._helper import get_config_slots, is_config
from cornflakes.decorator.config._load_config import create_file_loader
from cornflakes.decorator.config._load_config_group import create_group_loader
from cornflakes.decorator.config._protocols import Config, ConfigGroup
from cornflakes.decorator.config._write_config import write_config


def _parse_config_list(cfg, cfg_name: str, title: str):
    _ini_bytes = bytearray()
    has_list = isinstance(cfg, list)
    if is_config(cfg) and not has_list:
        return cfg.to_ini_bytes(cfg_name)
    elif has_list:
        for n, sub_cfg in enumerate(cfg):
            cfg_name = f"{cfg_name}_{n}"
            if is_config(sub_cfg) and hasattr(sub_cfg, "section_name"):
                cfg_name = sub_cfg.section_name
            _ini_bytes.extend(_parse_config_list(sub_cfg, cfg_name, title))
        return _ini_bytes
    else:
        logging.warning(f"The Value {cfg_name} of {title} be in a child config class!")
        return b""


def to_ini_bytes(
    self, title: Optional[str] = None
) -> bytearray:  # TODO: implement more type_to_str feature -> date format etc.
    """Method to write an instance of the main config class of the module into a ini bytearray."""
    _ini_bytes = bytearray()
    has_lists = isinstance(self, list)
    is_config = hasattr(self, "__config_sections__")
    if is_config and not has_lists:
        _ini_bytes.extend(bytes(f"[{title}]\n", "utf-8"))
        _ini_bytes.extend(
            bytes(
                "\n".join(
                    [
                        f'{cfg}="{type_to_str(getattr(self, cfg))}"'
                        for cfg in get_config_slots(self)
                        if cfg != "section_name"
                    ]
                ),
                "utf-8",
            )
        )
        _ini_bytes.extend(b"\n\n")
        return _ini_bytes

    for cfg_name in get_config_slots(self):
        cfg = getattr(self, cfg_name)
        _ini_bytes.extend(_parse_config_list(cfg, cfg_name, title))

    _ini_bytes.pop()  # at least remove second line-break

    return _ini_bytes


def to_ini(self, out_cfg: Optional[str] = None) -> Optional[bytearray]:
    """Method to write an instance of the main config class of the module into an ini file."""
    return write_config(self.to_ini_bytes(self.__class__.__name__.lower()), out_cfg)


def create_ini_file_loader(
    cls=None,
) -> Callable[..., Dict[str, Optional[Union[Config, List[Config]]]]]:
    """Method to create file loader for ini files."""

    def from_ini(*args, **kwargs) -> Dict[str, Optional[Union[Config, List[Config]]]]:
        return create_file_loader(cls=cls, loader=ini_load)(*args, **kwargs)  # type: ignore

    return from_ini


def create_ini_group_loader(
    cls=None,
) -> Callable[..., ConfigGroup]:
    """Method to create file loader for ini files."""

    def from_ini(*args, **kwargs) -> ConfigGroup:
        return create_group_loader(cls=cls, loader=ini_load)(*args, **kwargs)  # type: ignore

    return from_ini
