import re
from typing import List, Union

from cornflakes import ini_load
from cornflakes.logging import logger


def ini_config(  # noqa: C901
    config_cls=None,
    cfg_files: Union[str, List[str]] = "default.ini",
    cfg_sections: Union[str, List[str]] = None,
    use_regex: bool = False,
):
    """Config decorator to parse Ini Files and implements from_ini method to config-classes.

    :param config_cls: Config class
    :param cfg_files: Default config files
    :param cfg_sections: Default config sections
    :param use_regex: Flag to eval all sections by regex

    :returns: wrapped class or the wrapper itself with the custom default arguments if the config class is not

    """

    def wrapper(cls):
        """Wrapper function for the config decorator ini_config_decorator."""

        def to_dict(self) -> dict:
            return {key: getattr(self, key) for key in self.__slots__}

        def to_ini(self) -> str:
            return """
""".join(
                [
                    f"""
[{key}]
            {'''
'''.join([*([f"{sub_key}={getattr(self, sub_key)}"
             for sub_key in getattr(self, key).__slots__
             ] if hasattr(getattr(self, key), "__slots__") else f"{key}={getattr(self, key)}"
            for key in self.__slots__)])}
            """  # noqa: W291
                    for key in self.__slots__
                ]
            )

        def new(self, *args, **kwargs):
            # two chars missing in original of next line ...
            self.to_dict = to_dict
            self.to_ini = to_ini
            return super(cls, self).__new__(self)

        cls.__new__ = classmethod(new)

        def _create_config(config: dict, *args, **kwargs):
            error_keys = [key for key in kwargs if key not in cls.__slots__]
            if len(error_keys):
                logger.warning(f"Some variables in {cls.__name__} have no annotation or are not defined!")
                logger.warning(f"Please check Keys: {error_keys}")
            config.update({key: value for key, value in kwargs.items() if key in cls.__slots__})
            config_instance = cls(*args, **config)  # config_instance
            # config_instance.to_dict = to_dict
            # config_instance.to_ini = to_ini
            return config_instance

        def from_ini(
            files: Union[str, List[str]] = None, sections: Union[str, List[str]] = None, *args, **kwargs
        ) -> dict:
            """Config parser from ini files.

            :param files: Default config files
            :param sections: Default config sections
            :param args: Default configs to overwrite
            :param kwargs: Default configs to overwrite

            :returns: Nested Lists of Config Classes

            """
            if not sections:
                sections = cfg_sections
            if not files:
                files = cfg_files
            logger.debug(f"Load ini from file: {cfg_files} - sections: {sections} for config {cls.__name__}")
            if not use_regex:
                config_dict = ini_load(files, sections, keys=cls.__slots__[len(args) :])
                return {
                    file: {
                        section: _create_config(config_dict.get(file).get(section), *args, **kwargs)
                        for section in config_dict.get(file)
                    }
                    for file in config_dict
                }

            config_dict = ini_load(files, None, keys=cls.__slots__[len(args) :])
            regex = f'({"|".join(sections) if isinstance(sections, list) else sections})'
            return {
                file: {
                    section: _create_config(config_dict.get(file, {}).get(section, {}), *args, **kwargs)
                    for section in config_dict.get(file, {})
                    if bool(re.match(regex, section))
                }
                for file in config_dict
            }

        cls.from_ini = staticmethod(from_ini)  # class not dependent method

        return cls

    if config_cls:
        return wrapper(config_cls)
    return wrapper
