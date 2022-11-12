from inspect import getfile
from typing import Callable, Optional

from click import Group, style, version_option
import pkg_resources

from cornflakes.click import RichConfig, group
from cornflakes.decorator.config import Config


def click_cli(  # noqa: C901
    callback: Optional[Callable] = None,
    config: Optional[Config] = None,
    files: Optional[str] = None,
    loader: Optional[str] = None,
    *args,
    **kwargs,
):
    """Function that creates generic click CLI Object."""
    if not config:
        if not files:
            config = RichConfig(*args, **kwargs)
        elif loader in ["from_ini", "from_yaml"]:
            config = getattr(RichConfig, loader)(*args, **kwargs).popitem()[1]
        elif ".ini" in files:
            config = RichConfig.from_ini(files, *args, **kwargs).popitem()[1]
        elif ".yaml" in files:
            config = RichConfig.from_yaml(files, *args, **kwargs).popitem()[1]
        else:
            config = RichConfig(*args, **kwargs)

    def cli_wrapper(w_callback: Callable) -> Callable[..., Group]:
        if not callable(w_callback):
            return w_callback

        module = getfile(w_callback)
        cli_group = group(module.split(".", 1)[0], config=config)(w_callback)
        if config.VERSION_INFO:
            name = w_callback.__qualname__
            __version = "0.0.1"

            if hasattr(w_callback, "__module__"):
                module = w_callback.__module__.split(".", 1)[0]
                if module != "__main__":
                    __version = pkg_resources.get_distribution(module).version

            version_args = {
                "prog_name": name,
                "version": __version,
                "message": style(
                    f"\033[95m{module}\033" f"[0m \033[95m" f"Version\033[0m: \033[1m" f"{__version}\033[0m"
                ),
            }
            cli_group = version_option(**version_args)(cli_group)

        if cli_group.config.GLOBAL_OPTIONS:
            for option_obj in cli_group.config.GLOBAL_OPTIONS:
                cli_group.params.extend(option_obj.params)
        if config.CONTEXT_SETTINGS:
            cli_group.context_settings = config.CONTEXT_SETTINGS
        return cli_group

    if callback:
        return cli_wrapper(callback)
    return cli_wrapper
