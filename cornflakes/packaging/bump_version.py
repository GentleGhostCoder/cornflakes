#!/usr/bin/env python

import os
import pathlib
import subprocess
import sys

from click import Choice
from packaging import version

from cornflakes.cli import cli
from cornflakes.decorator.click import argument


@cli.command("bump")
@argument(
    "version_component",
    help="Level of the version component to bump",
    default="patch",
    type=Choice(["major", "minor", "patch"]),
    required=False,
)
def bump_version(level="patch"):  # noqa: C901
    """Bump version of the module for the given version level (major, minor, patch)."""
    latest_checkpoint = subprocess.check_output(["git", "rev-list", "--tags", "--max-count=1"]).decode().strip()

    # Get the current version from git tags
    current_version = subprocess.check_output(["git", "describe", "--tags", latest_checkpoint]).decode().strip()

    # Parse the current version
    parsed_version = version.parse(current_version)

    # Split the version string into major, minor, and patch numbers
    major, minor, patch = parsed_version.release

    # Increment the specified version component
    if level == "major":
        major += 1
        minor = 0
        patch = 0
    elif level == "minor":
        minor += 1
        patch = 0
    elif level == "patch":
        patch += 1
    else:
        print("Invalid version component. Please choose 'major', 'minor', or 'patch'.")
        return

    # Create the new version object
    new_version = version.Version(f"{major}.{minor}.{patch}")

    # Update the version in Python files
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)

                # Skip files in the "site-packages" directory
                if "site-packages" in file_path:
                    continue

                content = pathlib.Path(file_path).read_text()
                # Check if the file contains the string "# <<FORCE_BUMP>>"
                if "# <<FORCE_BUMP>>" in content:
                    # Increment the version number in the file
                    content = content.replace(parsed_version.public, str(new_version))

                    with open(file_path, "w") as f:
                        f.write(content)

    print(f"Version bumped to {new_version}")

    # Update the version in Poetry
    subprocess.call(["poetry", "version", str(new_version)])


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the version component to bump: 'major', 'minor', or 'patch'.")
    else:
        version_component = sys.argv[1]
        cli.main(["bump", version_component])
