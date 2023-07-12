# """Test cases for the cli decorator."""
# from click import command, group, option
# from click.testing import CliRunner
# import pytest
#
# from cornflakes import config
# from cornflakes.cli import cli
# from cornflakes.decorator.click import config_option
#
#
# @config
# class SomeConfig:
#     """Test CLI Config.
#
#     :cvar test_option: test option
#     """
#
#     test_option: str = "blub"
#
#
# @group("test")
# def some_group():
#     """Test CLI."""
#
#
# @command("test_command")
# @config_option(SomeConfig, config_file=True)
# @option("--test-arg", help="test arg", default="blub", required=False)
# def some_command(config, test_option, test_arg):
#     """Test CLI Command."""
#     # print(args)
#     # print(kwargs)
#     print(config)
#     print(test_option)
#     print(test_arg)
#
#
# some_group.add_command(some_command)
#
# cli.add_command(some_group)
#
#
# @pytest.fixture
# def runner() -> CliRunner:
#     """Fixture for invoking command-line interfaces."""
#     return CliRunner()
#
#
# def test_main_succeeds(runner: CliRunner) -> None:
#     """It exits with a status code of zero."""
#     result = runner.invoke(cli, ["test", "test_command"])
#     if result.exc_info:
#         assert result.exc_info[0] == TypeError or result.exc_info[0] == DeprecationWarning or result.exit_code == 0
