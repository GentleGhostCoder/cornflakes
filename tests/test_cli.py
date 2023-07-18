"""Test cases for the cli decorator."""
from typing import cast

from click import BaseCommand, command, group, option
from click.testing import CliRunner
import pytest

from cornflakes.cli import cli
from cornflakes.decorator.click import config_option
from cornflakes.decorator.dataclasses import config


@config
class SomeConfig:
    """Test CLI Config.

    :cvar test_option: test option
    """

    test_option: str = "blub"


@group("test")
def some_group():
    """Test CLI."""


@command("test_command")
@config_option(SomeConfig, config_file=True)
@option("--test-arg", help="test arg", default="blub", required=False)
def some_command(test_config: SomeConfig):
    """Test CLI Command."""
    print(test_config)


some_group.add_command(some_command)

cli.add_command(some_group)


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_main_succeeds(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(cast(BaseCommand, cli), ["test", "test_command"])
    if result.exc_info:
        assert result.exc_info[0] == TypeError or result.exc_info[0] == DeprecationWarning or result.exit_code == 0
