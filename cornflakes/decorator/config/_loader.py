from enum import Enum


class Loader(Enum):
    """Config Loader Enums."""

    INI_LOADER = "from_ini"
    YAML_LOADER = "from_yaml"
    DICT_LOADER = "from_dict"
