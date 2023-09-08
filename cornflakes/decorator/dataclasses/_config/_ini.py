import logging
from typing import Optional

from cornflakes.common import type_to_str
from cornflakes.decorator.dataclasses._config._load_config import create_file_loader
from cornflakes.decorator.dataclasses._config._write_config import write_config
from cornflakes.decorator.dataclasses._helper import get_loader_callback, get_not_ignored_slots, is_config
from cornflakes.types import Loader

logger = logging.getLogger(__name__)


def _parse_config_list(cfg, cfg_name: str, title: str):
    _ini_bytes = bytearray()
    is_list = isinstance(cfg, list)
    if is_config(cfg) and not is_list:
        return to_ini_bytes(cfg, cfg_name)
    elif is_list:
        for n, sub_cfg in enumerate(cfg):
            sub_cfg_name = cfg_name
            if is_config(sub_cfg) and (
                getattr(sub_cfg, "section_name", None) or getattr(sub_cfg, "__config_sections__", None)
            ):
                # if sub_cfg contains a section_name, use it instead of the default
                sub_cfg_name = getattr(sub_cfg, "section_name", sub_cfg.__config_sections__)
                if isinstance(sub_cfg_name, (list, tuple)):
                    sub_cfg_name = sub_cfg_name[0]

            if not sub_cfg_name:
                sub_cfg_name = f"{cfg_name}_{n}"

            _ini_bytes.extend(_parse_config_list(sub_cfg, sub_cfg_name, title))
        return _ini_bytes
    else:
        logger.warning(f"The Value {cfg_name} of {title} be in a child config class!")
        return b""


def to_ini_bytes(
    self, title: str
) -> Optional[bytearray]:  # TODO: implement more type_to_str feature -> date format etc.
    """Method to write an instance of the main config class of the module into a ini bytearray."""
    _ini_bytes = bytearray()
    has_lists = isinstance(self, list)
    if is_config(self) and not has_lists:
        _ini_bytes.extend(bytes(f"[{title}]\n", "utf-8"))
        _ini_bytes.extend(
            bytes(
                "\n".join(
                    [
                        f'{cfg}={f"{type_to_str(getattr(self, cfg))!r}" if getattr(self, cfg) is not None else ""}'
                        for cfg in get_not_ignored_slots(self)
                        if cfg != "section_name"
                    ]
                ),
                "utf-8",
            )
        )
        _ini_bytes.extend(b"\n\n")
        return _ini_bytes

    for cfg_name in get_not_ignored_slots(self):
        cfg = getattr(self, cfg_name)
        _ini_bytes.extend(_parse_config_list(cfg, cfg_name, title))

    if _ini_bytes:
        _ini_bytes.pop()  # at least remove second line-break

    return _ini_bytes


def to_ini(self, out_cfg: Optional[str] = None) -> Optional[bytearray]:
    """Method to write an instance of the main config class of the module into an ini file."""
    title = getattr(self, "section_name", getattr(self, "__config_sections__", self.__class__.__name__.lower()))
    if isinstance(title, (list, tuple)):
        title = title[0]
    return write_config(bytearray(to_ini_bytes(self, title) or b""), out_cfg)


def create_ini_file_loader(
    cls,
):
    """Method to create file loader for ini files."""

    def from_ini(*args, **kwargs):
        return create_file_loader(cls=cls, _loader_callback=get_loader_callback(Loader.INI), _instantiate=True)(*args, **kwargs)  # type: ignore

    return from_ini


# def create_ini_group_loader(
#     cls=None,
# ) -> Callable[..., ConfigGroup]:
#     """Method to create file loader for ini files."""
#
#     def from_ini(*args, **kwargs) -> ConfigGroup:
#         return create_group_loader(cls=cls)(*args, **kwargs)  # type: ignore
#
#     return from_ini
