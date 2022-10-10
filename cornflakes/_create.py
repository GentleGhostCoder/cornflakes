from cornflakes.common import click


@click.group("create")
def create_new_config():
    """Create config template."""  # noqa: D400, D401
