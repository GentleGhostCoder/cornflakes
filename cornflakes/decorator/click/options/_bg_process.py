import logging
import subprocess  # noqa: S404
import sys
from typing import Any, Union

from cornflakes.decorator.click.helper import get_command_name
from cornflakes.decorator.click.options._global import global_option
from cornflakes.decorator.click.rich import RichCommand, RichGroup

logger = logging.getLogger(__name__)


@global_option(
    ["-b", "--background-process"],
    is_flag=True,
    help="Run in Background without console logger.",
)
def bg_process_option(self: Union[RichCommand, RichGroup, Any], background_process: bool):
    """Default Option for running in background."""
    if background_process:
        print(self)
        command_name = get_command_name(self).replace(" ", "_").replace("-", "_")
        stdout_file = f"{command_name}.log"
        stderr_file = f"{command_name}_error.log"
        logger.debug(
            f"Method {self.callback.__name__} is running in background. "
            f"See logs at stdout: {stdout_file}, stderr: {stderr_file}."
        )
        stdout = open(stdout_file, "w")
        stderr = open(stderr_file, "w")

        # remove -b or --background-process from sys.argv
        sys.argv = [arg for arg in sys.argv if arg not in ["-b", "--background-process"]]

        logger.debug(f"Command: {' '.join(sys.argv)}")

        subprocess.Popen(  # noqa: S603
            sys.argv,
            stdout=stdout,
            stderr=stderr,
        )
        sys.exit(0)
