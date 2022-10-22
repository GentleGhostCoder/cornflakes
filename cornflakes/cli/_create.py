from click import style, version_option
import pkg_resources

from cornflakes import click
from cornflakes.logging import logger


@click.command("create")
@version_option(
    prog_name="cornflakes",
    version=pkg_resources.get_distribution("cornflakes").version,
    message=style(
        f"\033[95m{'cornflakes'}\033"
        f"[0m \033[95mVersion\033[0m: \033[1m"
        f"{pkg_resources.get_distribution('cornflakes').version}\033[0m"
    ),
)
def create_new_config():
    """Create config template."""  # noqa: D400, D401
    logger.info("call create")
    logger.debug("debug log?")
    for _ in range(10):
        print("blub")

    with open("/home/sgeist/arbeit/cornflakes/test.txt", "wb") as f:
        f.write(b"blub\n")
