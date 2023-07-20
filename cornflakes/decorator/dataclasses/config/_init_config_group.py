import logging
from typing import List, Optional

from cornflakes.decorator._wrap_kwargs import wrap_kwargs
from cornflakes.decorator.dataclasses._helper import (
    config_files,
    config_sections,
    dataclass_fields,
    fields,
    is_allow_empty,
    is_config,
    is_config_list,
    is_eval_env,
)


def _load_config_kwargs(
    cls,
    files: Optional[List[str]] = None,
    sections: Optional[List[str]] = None,
    eval_env: Optional[bool] = None,
    allow_empty: Optional[bool] = False,
    **kwargs,
):
    """Create default config arguments for a config-group class."""
    _files = files if isinstance(files, list) else [str(files)] if files else config_files(cls)
    default_config: dict = {}

    if not _files:
        return kwargs

    sections = sections if isinstance(sections, list) else [str(sections)] if sections else config_sections(cls)
    eval_env = eval_env or is_eval_env(cls)
    allow_empty = allow_empty or is_allow_empty(cls)

    for slot in fields(cls):
        slot_class = slot.type
        if is_config_list(slot_class):
            slot_class = slot.type.__args__[0]

        if is_config(slot_class):
            slot_config = slot_class.from_file(
                files=_files,
                sections=sections,
                eval_env=eval_env,
                allow_empty=allow_empty,
                **kwargs,
            )
            default_config.update(slot_config)

    if error_args := [key for key in default_config if key not in dataclass_fields(cls)]:
        logging.debug(f"The variables {error_args} in **{cls.__name__}** are not defined!")
        logging.debug("Use generate_group in build script to auto generate the config group!")

    return default_config


def wrap_init_config_group(cls):
    # Index.reset()
    # Index.group_indexing()
    # default_config = _load_config_kwargs(cls)
    # Index.group_indexing()
    # Index.reset()
    # prepare special slot types (e.g. Index)
    # default_config = evaluate_default_configs(cls, default_config)
    def pre_init_wrapper(init):
        @wrap_kwargs(init)
        def wrapper(
            self,
            files: Optional[List[str]] = None,
            sections: Optional[List[str]] = None,
            eval_env: Optional[bool] = None,
            allow_empty: Optional[bool] = False,
            **kwargs,
        ):
            # changed_kwargs = {
            #     key: value for key, value in kwargs.items() if repr(value) != repr(default_config.get(key))
            # }

            # if not changed_kwargs:
            #     return init(self, **kwargs.copy())

            files = files if isinstance(files, list) else [str(files)] if files else config_files(cls)

            if not files:
                return init(self, **kwargs)

            sections = sections if isinstance(sections, list) else [str(sections)] if sections else config_sections(cls)
            eval_env = eval_env or is_eval_env(cls)
            allow_empty = allow_empty or is_allow_empty(cls)
            return init(self, **_load_config_kwargs(cls, files, sections, eval_env, allow_empty, **kwargs))

        return wrapper

    setattr(cls, "__init__", pre_init_wrapper(cls.__init__))

    return cls
