#!/usr/bin/env python
"""Command-line interface."""

from cornflakes.common.cli import cli


def main(*args, **kwargs):
    """Main CLI Entrypoint Method."""
    cli(*args, **kwargs)


if __name__ == "__main__":
    main()  # pragma: no cover
