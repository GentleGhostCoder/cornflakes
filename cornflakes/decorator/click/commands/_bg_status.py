import os
from os.path import exists
import re
import sys
from typing import Optional, Union

from click import Command
from rich.syntax import Syntax
from rich.table import Table

from cornflakes.decorator.click._command import command
from cornflakes.decorator.click.rich import RichCommand, argument


def _analyze_logs(file, files: list, error_list: list, warning_list: list):
    """Analyze log files.

    :param file: log file
    :param files: list of log files
    :param error_list: list of errors
    :param warning_list: list of warnings

    :return: length of logs
    """
    logs_len = -1
    if exists(file):
        files.append(file)
        with open(file) as f:
            logs = f.read()
            if not logs:
                return 0
            logs = logs.split("\n")
            logs_len += len(logs) + 1
            warning_list.extend([line for line in logs if "WARNING" in line.upper()])
            error_list.extend([line for line in logs if "ERROR" in line.upper()])

    return logs_len


def _get_status_msg(process_patterns, exclude_pattern=None):
    """Get status message of all running processes.

    :param process_patterns: list of process patterns to search for
    :param exclude_pattern: list of patterns to exclude from search

    :return: list of status messages
    """
    processes = {}
    for process_pattern in process_patterns:
        process_msgs = re.sub(
            r"(\d{1,5})?.*python -c import sys;(.+?)\n?",
            "\\1\\2",
            os.popen(f"ps aux | grep '{process_pattern}' " "| awk '{print $2,$11,$12,$13,$14,$15}'").read(),
        ).split("\n")
        for process_msg in process_msgs:
            process_msg = process_msg.strip()
            if not process_msg:
                continue
            process_msg = process_msg.split(" ", 1)
            if not exclude_pattern:
                processes[process_msg[0]] = process_msg[-1]
                continue
            if not any([ex in process_msg for ex in exclude_pattern]):
                processes[process_msg[0]] = process_msg[-1]
    return processes


@command("stop")
@argument("id", type=str, required=False, default=None)
def command_stop(id: Optional[str]):
    """Default Command to stop all running processes stated from the parent group."""
    if id is None:
        os.system(f"kill $(ps aux | grep '{sys.argv[0]}' " "| awk '{print $2}')")
        return

    status = _get_status_msg([sys.argv[0]], ["grep", "aux", "status"])
    os.system(f"kill {status[id][0]}")


@command("status")
def command_status(self: Union[RichCommand, Command]):
    """Default Command to get status Table of all running processes stated from the parent group."""

    group_name = self.parent.name.replace(" ", "_").replace("-", "_")

    log_dir = f".log_{group_name}"

    if not os.path.exists(log_dir):
        return

    log_files = []
    for log_file in os.listdir(log_dir):
        log_file = f'{log_dir}/{log_file.replace("stderr", "stdout")}'
        if log_file not in log_files:
            log_files.append(log_file)

    if not log_files:
        return

    table = Table(title="core Status")
    table.add_column("ID", justify="right", style="red", no_wrap=True)
    table.add_column("PID", justify="right", style="yellow", no_wrap=True)
    table.add_column("COMMAND", justify="right", style="cyan", no_wrap=True)
    table.add_column("STATUS", style="magenta")
    table.add_column("LOG-FILES", justify="right", no_wrap=True)
    table.add_column("ERR", justify="right", no_wrap=True)
    table.add_column("WARN", justify="right", no_wrap=True)
    table.add_column("STDERR", justify="right", no_wrap=True)
    table.add_column("STDOUT", justify="right", no_wrap=True)

    processes = _get_status_msg([sys.argv[0]], ["grep", "aux", "status"])

    idx = 0
    for stdout_file in log_files:
        stderr_file = stdout_file.replace("_stderr_", "_stdout_")
        pid = stdout_file.split("_stdout_", 1)[-1].split("_", 1)[0]
        is_running = pid in processes
        command = processes[pid] if is_running else "-"
        status = "RUNNING" if is_running else "NOT RUNNING"
        stat = [idx, pid, command, status]
        idx += 1

        files = []
        error_list = []
        warning_list = []

        stderr_log_len = _analyze_logs(stderr_file, files, error_list, warning_list)
        stdout_log_len = _analyze_logs(stdout_file, files, error_list, warning_list)
        if stderr_log_len == -1 and stdout_log_len == -1:
            continue

        stat.append(str(files))

        stat.append(str(len(error_list) or "-"))
        stat.append(str(len(warning_list) or "-"))
        stat.append(str(stderr_log_len or "-"))
        stat.append(str(stdout_log_len or "-"))

        table.add_row(*[Syntax(str(s), "python", line_numbers=False, background_color="default") for s in stat])

    self.console.print(table)
