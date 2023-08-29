from inspect import getfile
import logging
from os.path import abspath
import subprocess  # noqa: S404
import sys
from typing import Any, Union

from cornflakes.decorator.click.options._global import global_option
from cornflakes.decorator.click.rich import RichCommand, RichGroup


@global_option(
    ["-b", "--background-process"],
    is_flag=True,
    # option_group="Basic Options",
    help="Run in Background without console logger.",
)
def bg_process_option(self: Union[RichCommand, RichGroup, Any], background_process: bool, *func_args, **func_kwargs):
    """Default Option for running in background."""
    if background_process:
        stdout_file = f"{self.callback.__name__}.log"
        stderr_file = f"{self.callback.__name__}_error.log"
        logging.debug(
            f"Method {self.callback.__name__} is running in background. "
            f"See logs at stdout: {stdout_file}, stderr: {stderr_file}."
        )
        stdout = open(stdout_file, "w")
        stderr = open(stderr_file, "w")

        command = (
            f"import sys; exec(open("
            f"{abspath(getfile(self.callback))!r}).read());"
            f"{self.callback.__name__}(*{func_args},**{func_kwargs});"
        )

        logging.debug(f"Python Command: {command}")

        subprocess.Popen(  # noqa: S603
            [
                sys.executable,
                "-c",
                command,
            ],
            stdout=stdout,
            stderr=stderr,
        )
        sys.exit(0)
