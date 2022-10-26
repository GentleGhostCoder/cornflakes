from click import style, version_option
import pkg_resources

from cornflakes.click import command, group, pass_context
from cornflakes.logging import logger


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


@command("test")
def test(parent):  # verbose, background_process, self, parent
    """Test click."""
    logger.info("call create")
    logger.debug("debug log?")
    for _ in range(5):
        parent.console.print("[blue]HI")


create_new_config.add_command(test)
