"""cornflakes CLI.
__________________________________

.. currentmodule:: cornflakes.cli

.. autosummary::
   :toctree: _generate

    create_new_config
"""  # noqa: RST303 D205
from cornflakes.click import argument, command


@command("test")
@argument("test", nargs=1, help="help")
def test(test):
    """Test CLI."""
    print(test)
