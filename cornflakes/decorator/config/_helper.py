def is_config(cls):
    """Method to return flag that class is a config class."""
    return hasattr(cls, "__config_sections__")


def is_group(cls):
    """Method to return flag that class is a config group class."""
    return not hasattr(cls, "__config_sections__") and hasattr(cls, "__config_files__")


def is_config_list(cls):
    """Method to return flag that the object is a list of configs."""
    return getattr(cls, "__config_list__", False) or (
        hasattr(cls, "__args__") and getattr(cls.__args__[0], "__config_list__", False)
    )


def allow_empty(cls):
    """Method to return flag that the config class can be empty."""
    return getattr(cls, "__allow_empty__", False)


def pass_section_name(cls):
    """Method to return flag that the config has section_name in slots, so that the section title is passed in."""
    return "section_name" in cls.__dataclass_fields__.keys()
