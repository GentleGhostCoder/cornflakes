"""cornflakes CLI.
__________________________________

.. currentmodule:: cornflakes.cli

.. autosummary::
   :toctree: _generate

    create_new_config
"""  # noqa: RST303 D205
from cornflakes import config
from cornflakes.click import command, auto_option


@config
class Test:
    """Test CLI Config."""

    test: str = "blub"


@command("test")
@auto_option(Test)
def test(config):
    """Test CLI."""
    print(config)
