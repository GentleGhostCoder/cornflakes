"""cornflakes CLI.
__________________________________

.. currentmodule:: cornflakes.cli

.. autosummary::
   :toctree: _generate

"""  # noqa: RST303 D205
# from click import option, echo

from cornflakes import config as config_wrapper
from cornflakes.click import auto_option, group


# argument
#
# import click_completion
# import os
#
# import click_completion.core
#
#
# def custom_startswith(string, incomplete):
#     """A custom completion matching that supports case insensitive matching"""
#     if os.environ.get('_CLICK_COMPLETION_COMMAND_CASE_INSENSITIVE_COMPLETE'):
#         string = string.lower()
#         incomplete = incomplete.lower()
#     return string.startswith(incomplete)
#
#
# click_completion.core.startswith = custom_startswith
# click_completion.init()
#
# cmd_help = """Shell completion for click-completion-command
# Available shell types:
# \b
#   %s
# Default type: auto
# """ % "\n  ".join('{:<12} {}'.format(k, click_completion.core.shells[k]) for k in sorted(
#     click_completion.core.shells.keys()))
#
#
# @group("completion", help=cmd_help)
# def completion():
#     pass
#
#
# @completion.command()
# @option('-i', '--case-insensitive/--no-case-insensitive', help="Case insensitive completion")
# @argument('shell', required=False, type=click_completion.DocumentedChoice(click_completion.core.shells))
# def show(shell, case_insensitive):
#     """Show the click-completion-command completion code"""
#     extra_env = {'_CLICK_COMPLETION_COMMAND_CASE_INSENSITIVE_COMPLETE': 'ON'} if case_insensitive else {}
#     echo(click_completion.core.get_code(shell, extra_env=extra_env))
#
#
# @completion.command()
# @option('--append/--overwrite', help="Append the completion code to the file", default=None)
# @option('-i', '--case-insensitive/--no-case-insensitive', help="Case insensitive completion")
# @argument('shell', required=False, type=click_completion.DocumentedChoice(click_completion.core.shells))
# @argument('path', required=False)
# def install(append, case_insensitive, shell, path):
#     """Install the click-completion-command completion"""
#     extra_env = {'_CLICK_COMPLETION_COMMAND_CASE_INSENSITIVE_COMPLETE': 'ON'} if case_insensitive else {}
#     shell, path = click_completion.core.install(shell=shell, path=path, append=append, extra_env=extra_env)
#     echo('%s completion installed in %s' % (shell, path))
#


@config_wrapper
class Test:
    """Test CLI Config."""

    test: str = "blub"


@group("test")
@auto_option(Test)
def test(config):
    """Test CLI."""
    print(config)
