"""Command-line interface."""
from cornflakes.cli.entrypoint import cli
from cornflakes.cli.bump import bump_version
from cornflakes.cli.update import update_deps

__all__ = ["cli", "bump_version", "update_deps"]
