import os

from cornflakes.decorator.dataclasses._config._load_config import create_file_loader


def create_dict_file_loader(
    cls,
):
    """Method to create file loader for passed dict."""

    def from_dict(*args, config_dict=None, **kwargs):
        if not config_dict:
            config_dict = {}
        default_kwargs = {}
        if cls.__eval_env__:
            default_kwargs.update(
                {key: os.environ[key] for key in cls.__dataclass_fields__.keys() if key in os.environ}
            )
        default_kwargs.update(kwargs)
        return create_file_loader(cls=cls, _instantiate=True)(*args, config_dict=config_dict, **default_kwargs)

    return from_dict
