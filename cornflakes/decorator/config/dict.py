import os
from typing import Any, Callable, Dict, List, Optional, Union

from cornflakes.decorator.config._load_config import create_file_loader
from cornflakes.decorator.types import Config


def create_dict_file_loader(
    cls: Union[Config, Any],
) -> Callable[..., Dict[str, Optional[Union[Config, List[Config], Any]]]]:
    """Method to create file loader for passed dict."""

    def from_dict(*args, config_dict=None, **kwargs) -> Dict[str, Optional[Union[Config, List[Config], Any]]]:
        if not config_dict:
            config_dict = {}
        default_kwargs = {}
        if cls.__eval_env__:
            default_kwargs.update(
                {key: os.environ[key] for key in cls.__dataclass_fields__.keys() if key in os.environ.keys()}
            )
        default_kwargs.update(kwargs)
        return create_file_loader(cls=cls)(*args, config_dict=config_dict, **default_kwargs)

    return from_dict
