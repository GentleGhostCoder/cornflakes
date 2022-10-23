from inspect import getfile
from os.path import abspath
import subprocess  # noqa: S404
import sys

from cornflakes.click.options._global import global_option
from cornflakes.logging import logger


@global_option(
    ["-b", "--background-process"],
    is_flag=True,
    help="Run in Background without console logger.",
)
def bg_process_option(background_process, cls, *func_args, **func_kwargs):
    """Default Option for running in background."""
    if background_process:
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
                    f"{abspath(getfile(cls))}').read());"
                    f"{cls.__name__}(*{func_args},**{func_kwargs});"
                ),
            ],
            stdout=stdout,
            stderr=stderr,
        )
        quit(0)
