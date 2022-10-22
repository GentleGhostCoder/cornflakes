from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Union

from cornflakes import ini_load
from cornflakes.decorator._add_dataclass_slots import add_slots
from cornflakes.decorator.config._dict import to_dict
from cornflakes.decorator.config._ini import to_ini, to_ini_bytes
from cornflakes.decorator.config._yaml import to_yaml, to_yaml_bytes
from cornflakes.logging import logger


def config_group(  # noqa: C901
    config_cls=None,
    files: Union[str, List[str]] = None,
    *args,
    loader: Callable[
        [
            Union[
                str,
                List[str],
                Dict[str, Union[str, List[str]]],
                Optional[Union[str, List[str], Dict[str, Union[str, List[str]]]]],
                Optional[Union[str, List[str], Dict[str, Union[str, List[str]]]]],
                Optional[Union[str, List[str], Dict[str, str]]],
            ]
        ],
        Dict,
    ] = ini_load,
    **kwargs,
):
    """Config decorator with a Subset of configs to parse Ini Files.

    :param config_cls: Config class
    :param files: Default config files
    :param loader: Config Loader (ini_load, yaml_load)
    :param args: Default configs to overwrite dataclass args
    :param kwargs: Default configs to overwrite dataclass args

    :returns: wrapped class or the wrapper itself with the custom default arguments if the config class is not

    """

    def wrapper(cls):

        cls = add_slots(dataclass(cls, *args, **kwargs))
        cls.__config_files__ = files

        # Check __annotations__
        if not hasattr(cls, "__annotations__"):
            return cls

        def _new(self, *new_args, **new_kwargs):
            # two chars missing in original of next line ...
            self.to_dict = to_dict
            self.to_ini = to_ini
            self.to_yaml = to_yaml
            self.to_yaml_bytes = to_yaml_bytes
            self.to_ini_bytes = to_ini_bytes
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
                files = cls.__config_files__

            config_dict = loader({None: files})
            logger.debug(f"Read config with sections: {config_dict.keys()}")

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
