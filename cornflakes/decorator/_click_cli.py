from inspect import getfile
from typing import Callable

from click import Group

from cornflakes.click import RichConfig, group
from cornflakes.decorator.config import INI_LOADER, YAML_LOADER


def click_cli(  # noqa: C901
    callback: Callable = None, config: RichConfig = None, files: str = None, loader: str = None, *args, **kwargs
):
    """Function that creates generic click CLI Object."""
    if not config:
        if not files:
            config = RichConfig(*args, **kwargs)
        elif loader in [INI_LOADER, YAML_LOADER]:
            config = getattr(RichConfig, loader)(*args, **kwargs).popitem()[1]
        elif ".ini" in files:
            config = RichConfig.from_ini(files, *args, **kwargs).popitem()[1]
        elif ".yaml" in files:
            config = RichConfig.from_ini(files, *args, **kwargs).popitem()[1]
        else:
            config = RichConfig(*args, **kwargs)

    def cli_wrapper(w_callback: Callable) -> Callable[..., Group]:
        if not callable(w_callback):
            return w_callback

        module = getfile(w_callback)
        if hasattr(w_callback, "__module__"):
            module = w_callback.__module__.split(".", 1)[0]

        cli_group = group(module.split(".", 1)[0], config=config)(w_callback)

        if cli_group.config.GLOBAL_OPTIONS:
            for option_obj in cli_group.config.GLOBAL_OPTIONS:
                cli_group.params.extend(option_obj.params)
        if config.CONTEXT_SETTINGS:
            cli_group.context_settings = config.CONTEXT_SETTINGS
        return cli_group

    if callback:
        return cli_wrapper(callback)
    return cli_wrapper
