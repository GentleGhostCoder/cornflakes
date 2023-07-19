import logging
from typing import List, Optional

from cornflakes import ini_load
from cornflakes.decorator._wrap_kwargs import wrap_kwargs
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


def _load_config_kwargs(
    cls,
    default_loader,
    files: Optional[List[str]] = None,
    sections: Optional[List[str]] = None,
    eval_env: Optional[bool] = None,
    allow_empty: Optional[bool] = False,
    **kwargs,
):
    """Create default config for a config class."""
    _files = files if isinstance(files, list) else [str(files)] if files else config_files(cls)

    if not _files:
        return kwargs

    sections = sections if isinstance(sections, list) else [str(sections)] if sections else config_sections(cls)
    eval_env = eval_env or is_eval_env(cls)
    allow_empty = allow_empty or is_allow_empty(cls)

    default_config = default_loader(
        files=_files,
        sections=sections,
        eval_env=eval_env,
        allow_empty=allow_empty,
        **kwargs,
    ).popitem()[1]

    if is_config_list(cls):
        default_config = {**default_config[0]}
        # When the config generates a list (with the `is_list` parameter), we use the first config only and log a warning that the user should use the `config_group` decorator that includes the config-list or to call the from_file method instead.
        logging.debug(
            f"Config class **{cls.__name__}** generates a list of configs."
            f"You can use the `config_group` decorator that includes the config-list or to call the from_file method to load the configs."
            f"The normal instantiation of the config class will only use the first config in the list."
        )
        default_config.update(kwargs)

    _required_keys = dataclass_required_keys(cls)

    if is_eval_env(cls):
        default_config.update(get_env_vars(cls))
    if missing_keys := [key for key in _required_keys if key not in default_config.keys()]:
        raise ValueError(
            f"Missing required values for keys {missing_keys} for dataclass {cls.__name__} in configs {_files}!\n"
            "Please provide correct config files or environment variables!\n"
            "You can also set init_default_config=False to disable the direct class instantiation from config."
        )

    return default_config


def wrap_init_default_config(cls):
    """Decorator to initialize a Config class from a file directly (without from_file or config_group)."""

    default_loader = create_file_loader(
        cls, _loader_callback=getattr(cls, Constants.config_decorator.DEFAULT_LOADER, ini_load), _instantiate=False
    )
    default_config = _load_config_kwargs(cls, default_loader)

    # prepare special slot types (e.g. Index)
    # default_config = evaluate_default_configs(cls, default_config)

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
                return init(self, **kwargs.copy())

            changed_kwargs = {
                key: value for key, value in kwargs.items() if repr(value) != repr(default_config.get(key))
            }

            if not changed_kwargs:
                # If no kwargs are changed, we can use the default config
                config_result = init(self, **kwargs.copy())
                return config_result

            return init(
                self,
                **_load_config_kwargs(
                    cls,
                    default_loader,
                    files=files,
                    sections=sections,
                    eval_env=eval_env,
                    allow_empty=allow_empty,
                    **changed_kwargs,
                ),
            )

        return wrapper

    setattr(cls, "__init__", pre_init_wrapper(cls.__init__))

    return cls
