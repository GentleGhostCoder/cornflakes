import logging
from typing import List, Optional

from cornflakes import ini_load
from cornflakes.decorator import wrap_kwargs
from cornflakes.decorator.dataclasses._helper import (
    config_files,
    config_sections,
    dataclass_required_keys,
    get_env_vars,
    is_allow_empty,
    is_config_list,
    is_eval_env,
)
from cornflakes.decorator.dataclasses.config._load_config import create_file_loader
from cornflakes.types import Constants


def _create_default_config(cls, default_loader):
    """Create default config for a config class."""

    _files = getattr(cls, Constants.config_decorator.FILES, [])
    default_config = {}

    if _files:
        default_config = default_loader(
            files=_files,
            sections=getattr(cls, Constants.config_decorator.SECTIONS, []),
            eval_env=getattr(cls, Constants.dataclass_decorator.EVAL_ENV, False),
            allow_empty=getattr(cls, Constants.config_decorator.ALLOW_EMPTY, False),
        ).popitem()[1]

        if is_config_list(cls):
            default_config = default_config[0]

        default_config = {**default_config}
        logging.debug(f"Overwrite Class init with default config for {cls.__name__}: {default_config.keys()}")

    _required_keys = dataclass_required_keys(cls)

    if is_eval_env(cls):
        default_config.update(get_env_vars(cls))
    missing_keys = set(_required_keys) - set(default_config.keys())
    if missing_keys:
        raise ValueError(
            f"Missing required values for keys {missing_keys} for dataclass {cls.__name__} in configs {_files}!\n"
            "Please provide correct config files or environment variables!\n"
            "You can also set init_default_config=False to disable the direct class instantiation from config."
        )


def wrap_init_default_config(cls):
    """Decorator to initialize a Config class from a file directly (without from_file or config_group)."""

    default_loader = create_file_loader(
        cls, _loader_callback=getattr(cls, Constants.config_decorator.DEFAULT_LOADER, ini_load), _instantiate=False
    )
    default_config = _create_default_config(cls, default_loader)

    def pre_init_wrapper(init):
        @wrap_kwargs(init, **default_config)
        def wrapper(
            self,
            files: Optional[List[str]] = None,
            sections: Optional[List[str]] = None,
            eval_env: Optional[bool] = None,
            allow_empty: Optional[bool] = False,
            _load_default: bool = True,
            **kwargs,
        ):
            if not _load_default:
                return init(self, **kwargs)

            changed_kwargs = {key: value for key, value in kwargs.items() if value is not default_config.get(key)}

            if not changed_kwargs:
                return init(self, **default_config)

            files = files or config_files(cls)
            sections = sections or config_sections(cls)
            eval_env = eval_env or is_eval_env(cls)
            allow_empty = allow_empty or is_allow_empty(cls)

            if not files:
                # No files provided, return default config
                return init(self, **kwargs)

            config = default_loader(
                files=files,
                sections=sections,
                eval_env=eval_env,
                config_dict=None,
                allow_empty=allow_empty,
                **changed_kwargs,
            ).popitem()[1]

            if is_config_list(cls):
                logging.warning(
                    f"Config class **{cls.__name__}** generates a list of configs. "
                    f"Please use the `config_group` decorator that includes the config-list or to call the from_file method instead."
                )
                config = {**config[0]}
            return init(self, **config)

        return wrapper

    setattr(cls, "__init__", pre_init_wrapper(cls.__init__))

    return cls