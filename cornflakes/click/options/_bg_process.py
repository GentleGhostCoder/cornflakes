from inspect import getfile
from os.path import abspath
import subprocess  # noqa: S404
import sys
from typing import Callable

from cornflakes.click.options._global import global_option
from cornflakes.logging import logger


@global_option(
    ["-b", "--background-process"],
    is_flag=True,
    help="Run in Background without console logger.",
)
def bg_process_option(self: Callable[..., None], background_process: bool, *func_args, **func_kwargs):
    """Default Option for running in background."""
    if background_process:
        stdout_file = f"{self.__name__}.logs"
        stderr_file = f"{self.__name__}_error.log"
        logger.debug(
            f"Method {self.__name__} is running in background. "
            f"See logs at stdout: {stdout_file}, stderr: {stderr_file}."
        )
        stdout = open(stdout_file, "w")
        stderr = open(f"{self.__name__}_error.logs", "w")
        subprocess.Popen(  # noqa: S603
            [
                sys.executable,
                "-c",
                (
                    f"import sys; exec(open('"
                    f"{abspath(getfile(self))}').read());"
                    f"{self.__name__}(*{func_args},**{func_kwargs});"
                ),
            ],
            stdout=stdout,
            stderr=stderr,
        )
        quit(0)
