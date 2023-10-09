from datetime import datetime
import logging
import os
import subprocess  # noqa: S404
import sys
import tempfile
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
        tempfile.NamedTemporaryFile("w")

        command = get_command_name(self)
        is_group = len(command.split(" ", 1)) > 1
        if not is_group:
            command = f"{command} {self.callback.__name__}"
        group, command = command.split(" ", 1)
        log_dir = f".log_{group}".replace(" ", "_").replace("-", "_")

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        command_name = command.replace(" ", "_").replace("-", "_")

        date_str = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

        # try to guess the process id of the background process (not 100% accurate)
        pid = os.getpid() + 1

        stdout_file = f"{log_dir}/{command_name}_stdout_{pid}_{date_str}.log"
        stderr_file = f"{log_dir}/{command_name}_stderr_{pid}_{date_str}.log"
        logger.debug(
            f"Method {self.callback.__name__} is running in background. "
            f"See logs at stdout: {stdout_file}, stderr: {stderr_file}."
        )

        # remove -b or --background-process from sys.argv
        sys.argv = [arg for arg in sys.argv if arg not in ["-b", "--background-process"]]
        logger.debug(f"Command: {' '.join(sys.argv)}")

        with open(stdout_file, "w") as stdout, open(stderr_file, "w") as stderr:
            process = subprocess.Popen(sys.argv, stdout=stdout, stderr=stderr, bufsize=-1, start_new_session=False)
            try:
                process.communicate()
            except Exception as e:
                logger.error(f"Error communicating with subprocess: {e}")
            sys.exit(0)
