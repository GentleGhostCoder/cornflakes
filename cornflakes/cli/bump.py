#!/usr/bin/env python
from distutils.version import LooseVersion
import os
import pathlib
import subprocess
import sys

from click import Choice

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
    parsed_version = LooseVersion(current_version)

    # Split the version string into major, minor, and patch numbers
    major, minor, patch = map(int, parsed_version.vstring.split("."))

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
    new_version = LooseVersion(f"{major}.{minor}.{patch}")

    # Update the version in Python files
    for root, dirs, files in os.walk("."):
        for file in files:
            if (
                file.endswith(".py")
                or file.endswith(".yml")
                or file.endswith(".yaml")
                or file.endswith(".ini")
                or file.endswith(".toml")
            ):
                file_path = os.path.join(root, file)

                # Skip files in the "site-packages" directory
                if (
                    "site-packages" in file_path
                    or ".nox" in file_path
                    or ".venv" in file_path
                    or ".git" in file_path
                    or ".tox" in file_path
                    or ".pytest_cache" in file_path
                    or ".mypy_cache" in file_path
                    or ".eggs" in file_path
                    or ".idea" in file_path
                    or ".vscode" in file_path
                    or ".ruff_cache" in file_path
                    or ".mypy_cache" in file_path
                ):
                    continue

                content = pathlib.Path(file_path).read_text()
                # Check if the file contains the string "# <<FORCE_BUMP>>"
                if "<<FORCE_BUMP>>" in content:
                    # Increment the version number in the file
                    content = content.replace(str(parsed_version), str(new_version))
                    print(f"Updating version in {file_path}")
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
