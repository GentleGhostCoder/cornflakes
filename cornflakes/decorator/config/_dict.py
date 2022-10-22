from cornflakes.decorator.config._load_config import create_file_loader
from cornflakes.decorator.config._load_config_group import create_group_loader


def to_dict(self) -> dict:
    """Method to convert Dataclass with slots to dict."""
    return {key: getattr(self, key) for key in self.__slots__}


def create_dict_file_loader(
    cls=None,
):
    """Method to create file loader for ini files."""

    def from_dict(config_dict):
        return create_file_loader(cls=cls)(config_dict=config_dict)

    return from_dict


def create_dict_group_loader(
    cls=None,
):
    """Method to create file loader for ini files."""

    def from_dict(config_dict):
        return create_group_loader(cls=cls)(config_dict=config_dict)

    return from_dict
