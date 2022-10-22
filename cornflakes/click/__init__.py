"""Click Extension for better CLI.
__________________________________
See referenced Code at https://github.com/ewels/rich-click.git

.. currentmodule:: cornflakes.click

.. autosummary::
    :toctree: _generate

    RichArg
    RichCommand
    RichGroup
    RichConfig
    verbose_option
    bg_process_option
"""  # noqa: RST303 D205
import inspect
import logging
import os
import sys
from typing import TYPE_CHECKING, Callable
import pkg_resources
from click import Option, option, style, version_option  # noqa: F401, F403
from click import argument as click_argument
from click import command as click_command
from click import group as click_group

from cornflakes.click._rich_argument import RichArg
from cornflakes.click._rich_command import RichCommand
from cornflakes.click._rich_group import RichGroup
from cornflakes.click._rich_config import Config as RichConfig
from cornflakes.logging import logger
import subprocess  # noqa: S404

if TYPE_CHECKING:
    from click import Choice, Path, params  # noqa: F401


def global_option(*option_args, **option_kwargs):
    _option = Option(*option_args, **option_kwargs)

    def global_option_decorator(option_func: Callable[..., None]):
        if not callable(option_func):
            return option_func

        if not hasattr(option_func, "params"):
            option_func.params = []
        option_func.params.append(_option)

        return option_func

    return global_option_decorator


@global_option(
    ["-v", "--verbose"],
    is_flag=True,
    help="Base logging level is set to logging.DEBUG.",
)
def verbose_option(verbose):
    """Default Option for verbose logging."""
    logger.setup_logging(default_level=verbose and logging.DEBUG, force=True)


@global_option(
    ["-b", "--background-process"],
    is_flag=True,
    help="Run in Background without console logger.",
)
def bg_process_option(background_process, cls, *func_args, **func_kwargs):
    """Default Option for running in background."""
    if background_process:
        print("background_process")
        stdout_file = f"{cls.__name__}.logs"
        stderr_file = f"{cls.__name__}_error.logs"
        logger.debug(
            f"Method {cls.__name__} is running in background. "
            f"See logs at stdout: {stdout_file}, stderr: {stderr_file}."
        )
        stdout = open(stdout_file, "w")
        stderr = open(f"{cls.__name__}_error.logs", "w")
        subprocess.Popen(  # noqa: S603
            [
                sys.executable,
                "-c",
                (
                    f"import sys; exec(open('"
                    f"{os.path.abspath(inspect.getfile(cls))}').read());"
                    f"{cls.__name__}(*{func_args},**{func_kwargs});"
                ),
            ],
            stdout=stdout,
            stderr=stderr,
        )
        quit(0)


def _global_option_wrapper(click_func, *wrap_args, **wrap_kwargs):
    # config = wrap_kwargs.pop("config", None)

    def global_option_click_decorator(func):

        # if config:
        #     def global_option_func_wrapper(*func_args, **func_kwargs):
        #         func_kwargs["cls"] = func
        #         logger.setup_logging(default_level=func_kwargs.get("verbose", False) and logging.DEBUG, force=True)
        #         print(func.__module__)
        #         print((True if config and config.GLOBAL_OPTIONS and func.__module__ != "cornflakes.click" else False))
        #         if config and config.GLOBAL_OPTIONS and func.__module__ != "cornflakes.click":
        #             for option_obj in config.GLOBAL_OPTIONS:
        #                 print(f"call {option_obj.__name__}")
        #                 option_obj(*func_args, **func_kwargs)
        #         return func(*func_args, **{key: value for key, value
        #                                    in func_kwargs.items() if key in func.__code__.co_varnames})
        #
        #     click_cls = click_func(*wrap_args, **wrap_kwargs)(global_option_func_wrapper)
        #     click_cls.config = config
        #     return click_cls

        click_cls = click_func(*wrap_args, **wrap_kwargs)(func)

        def click_callback(*func_args, **func_kwargs):
            func_kwargs["cls"] = func
            logger.setup_logging(default_level=func_kwargs.get("verbose", False) and logging.DEBUG, force=True)
            if click_cls.config and click_cls.config.GLOBAL_OPTIONS and func.__module__ != "cornflakes.click":
                for option_obj in click_cls.config.GLOBAL_OPTIONS:
                    option_obj(
                        *func_args,
                        **{key: value for key, value in func_kwargs.items() if key in option_obj.__code__.co_varnames},
                    )
            return func(
                *func_args, **{key: value for key, value in func_kwargs.items() if key in func.__code__.co_varnames}
            )

        click_cls.callback = click_callback
        return click_cls

    return global_option_click_decorator


def group(*args, cls=RichGroup, **kwargs) -> click_group:  # type: ignore
    """Group decorator function.

    Defines the group() function so that it uses the RichGroup class by default.
    """
    return _global_option_wrapper(click_group, *args, cls=cls, **kwargs)


def command(*args, cls=RichCommand, **kwargs) -> click_command:  # type: ignore
    """Command decorator function.

    Defines the command() function so that it uses the RichCommand class by default.
    """
    return _global_option_wrapper(click_command, *args, cls=cls, **kwargs)


def argument(*args, cls=RichArg, **kwargs) -> click_argument:  # type: ignore
    """Command decorator function.

    Defines the command() function so that it uses the RichCommand class by default.
    """
    return click_argument(*args, cls=cls, **kwargs)


def make_cli(
    module: str,
    *args,
    **kwargs,
):
    """Function that creates generic click CLI Object."""
    module = module.split(".", 1)[0]
    config = RichConfig(*args, **kwargs)

    @version_option(
        prog_name=module,
        version=pkg_resources.get_distribution(module).version,
        message=style(
            f"\033[95m{module}\033"
            f"[0m \033[95mVersion\033[0m: \033[1m"
            f"{pkg_resources.get_distribution(module).version}\033[0m"
        ),
    )
    @group(module.split(".", 1)[0], config=config)
    def cli():
        pass

    if cli.config.GLOBAL_OPTIONS:
        for option_obj in cli.config.GLOBAL_OPTIONS:
            cli.params.extend(option_obj.params)
    if config.CONTEXT_SETTINGS:
        cli.context_settings = config.CONTEXT_SETTINGS
    return cli


__all__ = [
    "make_cli",
    "verbose_option",
    "bg_process_option",
    "argument",
    "Choice",
    "option",
    "Path",
    "group",
    "command",
    "RichGroup",
    "RichCommand",
    "RichConfig",
]
