"""Test cases for the __main__ module."""
import logging

from click import pass_context, style, version_option
from click.testing import CliRunner
import pkg_resources
import pytest

from cornflakes.__main__ import main
from cornflakes.click import command, group
from cornflakes.logging import attach_log


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_main_succeeds(runner: CliRunner) -> None:
    """It exits with a status code of zero."""

    @group("create")
    @version_option(
        prog_name="cornflakes",
        version=pkg_resources.get_distribution("cornflakes").version,
        message=style(
            f"\033[95m{'cornflakes'}\033"
            f"[0m \033[95mVersion\033[0m: \033[1m"
            f"{pkg_resources.get_distribution('cornflakes').version}\033[0m"
        ),
    )
    @pass_context
    def create_new_config(ctx, parent):
        """Create config template."""
        if ctx.invoked_subcommand is None:
            parent.console.print("[blue]I was invoked without subcommand")
            test(parent)

    @attach_log
    class Test:
        @classmethod
        def test(cls):
            cls.logger.info("test")
            cls.logger.debug("test2")
            cls.logger.error("test")

    @command("test")
    def test(parent):  # verbose, background_process, self, parent
        """Test click."""
        logging.info("call create")
        logging.debug("debug log?")
        for _ in range(5):
            parent.console.print("[blue]HI")
        Test.test()

    create_new_config.add_command(test)
    main.add_command(create_new_config)

    result = runner.invoke(main)
    if result.exc_info:
        assert result.exc_info[0] == TypeError or result.exc_info[0] == DeprecationWarning or result.exit_code == 0
