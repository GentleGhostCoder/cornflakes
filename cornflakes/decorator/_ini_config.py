from dataclasses import dataclass
from decimal import Decimal
from os import path
import re
from typing import Any, Dict, List, Union

from cornflakes import ini_load
from cornflakes.decorator._add_dataclass_slots import add_slots
from cornflakes.logging import logger


def _type_to_str(f):
    """Function to convert python object to string -> fix scientific notation for float / Decimal."""
    string = str(f)
    if type(f) in [Decimal, float, int]:
        string = re.sub(r".*'(.+)'.*", "\\1", repr(f).lower())
        if re.match(r"^(-)?1e[+-][1-9]", string):  # detect scientific notation
            digits, exp = string.split("e")
            digits = digits.replace(".", "").replace("-", "")
            exp = int(exp)
            zero_padding = "0" * (abs(int(exp)) - 1)  # minus 1 for decimal point in the sci notation
            sign = "-" if f < 0 else ""
            if exp > 0:
                string = f"{sign}{digits}{zero_padding}.0"
            else:
                string = f"{sign}0.{zero_padding}{digits}"
    return string


def _to_dict(self) -> dict:
    return {key: getattr(self, key) for key in self.__slots__}


def _to_ini_bytes(self, title: str = None) -> bytearray:  # TODO: implement more type_to_str feature -> date format etc.
    """Method to write an instance of the main config class of the module into a bytearray."""
    _ini_bytes = bytearray()
    if any([not hasattr(getattr(self, cfg), "to_ini_bytes") for cfg in self.__slots__]):
        _ini_bytes.extend(bytes(f"[{title}]\n", "utf-8"))
        _ini_bytes.extend(
            bytes("\n".join([f'{cfg}="{_type_to_str(getattr(self, cfg))}"' for cfg in self.__slots__]), "utf-8")
        )
        _ini_bytes.extend(b"\n\n")
        return _ini_bytes

    for cfg_name in self.__slots__:
        cfg_value = getattr(self, cfg_name)
        if hasattr(cfg_value, "to_ini_bytes"):
            _ini_bytes.extend(cfg_value.to_ini_bytes(cfg_name))
        else:
            logger.warning(f"The Value {cfg_name} of {title} be in a child ini_config class!")

    _ini_bytes.extend(b"\n")
    return _ini_bytes


def _to_ini(self, out_cfg: str = None) -> Union[None, bytearray]:
    """Method to write an instance of the main config class of the module into an ini file."""
    _ini_bytes = _to_ini_bytes(self, self.__class__.__name__.lower())
    if not out_cfg:
        return _ini_bytes
    with open(path.abspath(path.expanduser(out_cfg)), "wb") as f:
        f.write(_ini_bytes)

    if not out_cfg:
        return _ini_bytes
    with open(path.abspath(path.expanduser(out_cfg)), "wb") as f:
        f.write(_ini_bytes)


def ini_group(  # noqa: C901
    config_cls=None,
    files: Union[str, List[str]] = None,
    *args,
    **kwargs,
):
    """Config decorator with a Subset of ini_configs to parse Ini Files.

    :param config_cls: Config class
    :param files: Default config files
    :param args: Default configs to overwrite dataclass args
    :param kwargs: Default configs to overwrite dataclass args

    :returns: wrapped class or the wrapper itself with the custom default arguments if the config class is not

    """

    def wrapper(cls):

        cls = add_slots(dataclass(cls, *args, **kwargs))
        cls.__ini_configs__ = files

        # Check __annotations__
        if not hasattr(cls, "__annotations__"):
            return cls

        def _new(self, *new_args, **new_kwargs):
            # two chars missing in original of next line ...
            self.to_ini = _to_ini
            self.to_ini_bytes = _to_ini_bytes
            return super(cls, self).__new__(self)

        cls.__new__ = classmethod(_new)

        def from_ini(
            files: Union[str, List[str], Dict[str, Union[str, List[str]]]] = None,
            *slot_args,
            **slot_kwargs,
        ) -> cls:
            """Config parser from ini files.

            :param files: Default config files
            :param slot_args: Default configs to overwrite passed class
            :param slot_kwargs: Default configs to overwrite passed class

            :returns: Nested Lists of Config Classes

            """
            if not files:
                files = cls.__ini_configs__

            config_dict = ini_load({None: files}, {None: None})

            for slot_class in list(cls.__annotations__.values())[len(slot_args) :]:
                if hasattr(slot_class, "from_ini"):
                    slot_kwargs.update(slot_class.from_ini(config_dict=config_dict))

            error_args = [key for key in slot_kwargs if key not in cls.__slots__]
            if error_args:
                logger.warning(f"The variables {error_args} in **{cls.__name__}** are not defined!")
                logger.warning("Use generate_group in build script to auto generate the config group!")

            return cls(*slot_args, **{key: value for key, value in slot_kwargs.items() if key not in error_args})

        cls.from_ini = staticmethod(from_ini)  # class not dependent method

        return cls

    if config_cls:
        return wrapper(config_cls)
    return wrapper


def ini_config(  # noqa: C901
    config_cls=None,
    files: Union[str, List[str]] = None,
    sections: Union[str, List[str]] = None,
    use_regex: bool = False,
    *args,
    **kwargs,
):
    """Config decorator to parse Ini Files and implements from_ini method to config-classes.

    :param config_cls: Config class
    :param files: Default config files
    :param sections: Default config sections
    :param use_regex: Flag to eval all sections by regex
    :param args: Default configs to overwrite dataclass args
    :param kwargs: Default configs to overwrite dataclass args

    :returns: wrapped class or the wrapper itself with the custom default arguments if the config class is not
    """

    def wrapper(cls):
        """Wrapper function for the config decorator ini_config_decorator."""
        # Check __annotations__
        if not hasattr(cls, "__annotations__"):
            logger.warning(f"{cls.__name__} missing annotations for values!")
            return cls

        # Check is ini_group
        if any([hasattr(slot, "__ini_config_sections__") for slot in cls.__annotations__.values()]):
            logger.warning(
                "Wrapper ini_config not working for a subset of ini_config classes. " "Please use ini_group instead."
            )
            return ini_group(cls)

        cls = add_slots(dataclass(cls, *args, **kwargs))
        cls.__ini_config_sections__ = sections
        cls.__ini_configs__ = files

        def _new(self, *new_args, **new_kwargs):
            # two chars missing in original of next line ...
            self.to_dict = _to_dict
            self.to_ini = _to_ini
            self.to_ini_bytes = _to_ini_bytes
            return super(cls, self).__new__(self)

        cls.__new__ = classmethod(_new)

        def _create_config(config: dict, *cls_args, **cls_kwargs):
            config.update(cls_kwargs)
            error_args = [key for key in config if key not in cls.__slots__]
            if error_args:
                logger.warning(f"Some variables in **{cls.__name__}** have no annotation or are not defined!")
                logger.warning(f"Please check Args: {error_args}")
            #  config_instance
            config_instance = cls(*cls_args, **{key: value for key, value in config.items() if key in cls.__slots__})
            return config_instance

        def from_ini(
            files: Union[str, List[str], Dict[str, Union[str, List[str]]]] = None,
            sections: str = None,
            config_dict: Dict[str, Any] = None,
            *slot_args,
            **slot_kwargs,
        ) -> dict:
            """Config parser from ini files.

            :param files: Default config files
            :param sections: Default config sections
            :param config_dict: Config dictionary to pass already loaded configs
            :param slot_args: Default configs to overwrite passed class
            :param slot_kwargs: Default configs to overwrite passed class

            :returns: Nested Lists of Config Classes

            """
            if not sections:
                sections = cls.__ini_config_sections__
            if not files:
                files = cls.__ini_configs__
            if not use_regex:
                logger.debug(f"Load ini from file: {files} - section: {sections} for config {cls.__name__}")
                if not config_dict:
                    config_dict = ini_load({None: files}, {None: sections}, keys=cls.__slots__[len(slot_args) :])
                return {sections: _create_config(config_dict, *slot_args, **slot_kwargs)}

            if not config_dict:
                config_dict = ini_load({None: files}, None, keys=cls.__slots__[len(slot_args) :])
                logger.debug(f"Read config with sections: {config_dict.keys()}")
            regex = f'({"|".join(sections) if isinstance(sections, list) else sections})'
            logger.debug(f"Load all configs that mach **{regex}**")
            return {
                section: _create_config(config_dict, *slot_args, **slot_kwargs)
                for section, config_dict in config_dict.items()
                if bool(re.match(regex, section))
            }

        cls.from_ini = staticmethod(from_ini)  # class not dependent method

        return cls

    if config_cls:
        return wrapper(config_cls)
    return wrapper
