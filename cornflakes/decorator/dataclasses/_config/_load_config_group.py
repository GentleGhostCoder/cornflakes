import logging

from cornflakes.decorator.dataclasses._helper import is_config, is_config_list, is_group

logger = logging.getLogger(__name__)


def create_group_loader(cls):
    """Config decorator to parse Ini Files and implements from_file method to config-group-classes.

    :param cls: Config class

    :returns: wrapped class or the wrapper itself with the custom default arguments if the config group class is not
    """
    if not is_group(cls):
        raise TypeError(f"Class {cls.__name__} is not a config group class!")

    def from_file(
        files=None,
        sections=None,
        config_dict=None,
        eval_env=None,
        allow_empty=None,
        *slot_args,
        **slot_kwargs,
    ):
        """Config parser from config files.

        :param files: Default config files
        :param sections: Default config sections
        :param config_dict: Config dictionary to pass already loaded configs
        :param slot_kwargs: Default configs to overwrite passed class
        :param eval_env: Flag to evaluate environment variables into default values.
        :param allow_empty: Flag that allows empty config result -> e.g. emtpy list
        :param slot_args: Default configs to overwrite passed class
        :param slot_kwargs: Default configs to overwrite passed class

        :returns: Nested Lists of Config Classes

        """
        if not files:
            files = cls.__config_files__

        for slot_class in list(getattr(cls, "__annotations__", {}).values())[len(slot_args) :]:
            if is_config_list(slot_class):
                slot_class = slot_class.__args__[0]
            if is_config(slot_class):
                setattr(slot_class, "__config_files__", [*getattr(slot_class, "__config_files__", []), *files])
                slot_kwargs.update(
                    slot_class.from_file(
                        files=files,
                        sections=sections,
                        config_dict=config_dict,
                        eval_env=eval_env,
                        allow_empty=allow_empty or cls.__allow_empty_config__,
                    )
                )

        error_args = [key for key in slot_kwargs if key not in cls.__dataclass_fields__]
        if error_args:
            logger.debug(f"The variables {error_args} in **{cls.__name__}** are not defined!")
            logger.debug("Use generate_group in build script to auto generate the config group!")

        return cls(*slot_args, **{key: value for key, value in slot_kwargs.items() if key not in error_args})

    return from_file  # class not dependent method
