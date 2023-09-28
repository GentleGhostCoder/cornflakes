from datetime import datetime
import logging
import os
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
        # Create a Popen object but don't start the subprocess yet
        process = subprocess.Popen(sys.argv, stdout=subprocess.PIPE, bufsize=-1, start_new_session=True)

        command = get_command_name(self)
        group, command = command.split(" ", 1)
        log_dir = f".log_{group}".replace(" ", "_").replace("-", "_")

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        command_name = command.replace(" ", "_").replace("-", "_")

        date_str = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

        stdout_file = f"{log_dir}/{command_name}_stdout_{process.pid}_{date_str}.log"
        stderr_file = f"{log_dir}/{command_name}_stderr_{process.pid}_{date_str}.log"
        logger.debug(
            f"Method {self.callback.__name__} is running in background. "
            f"See logs at stdout: {stdout_file}, stderr: {stderr_file}."
        )
        stdout = open(stdout_file, "a")
        stderr = open(stderr_file, "a")

        # remove -b or --background-process from sys.argv
        sys.argv = [arg for arg in sys.argv if arg not in ["-b", "--background-process"]]

        logger.debug(f"Command: {' '.join(sys.argv)}")
        process.stdout = stdout
        process.stderr = stderr
        process.communicate()
        sys.exit(0)
