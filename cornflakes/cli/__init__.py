"""cornflakes CLI.
__________________________________

.. currentmodule:: cornflakes.cli

.. autosummary::
   :toctree: _generate

"""  # noqa: RST303 D205
from cornflakes import config as config_wrapper
from cornflakes.click import command, auto_option


@config_wrapper
class Test:
    """Test CLI Config."""

    test: str = "blub"


@command("test")
@auto_option(Test)
def test(config):
    """Test CLI."""
    print(config)
