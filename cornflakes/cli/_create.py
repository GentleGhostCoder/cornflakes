from cornflakes import click
from cornflakes.logging import logger


@click.command("create")
def create_new_config():
    """Create config template."""  # noqa: D400, D401
    logger.info("call create")
    logger.debug("debug log?")
