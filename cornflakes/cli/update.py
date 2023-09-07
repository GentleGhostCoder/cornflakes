from distutils.version import LooseVersion
import pathlib
import re
import subprocess
from typing import Dict, cast

import toml

from cornflakes.cli import cli


def _parse_version_dependency(version_str):
    if match := re.match(r"(>=|<=|>|<|\^)(\d+.*)", version_str):
        return match[1], match[2]
    else:
        return None, None


def _update_deps(name: str, latest_version: str, t: Dict, c: str) -> str:  # noqa: C901
    def update(deps: Dict, content_lines: list) -> str:
        for d in deps:
            v = deps[d]
            if isinstance(v, dict):
                v = v.get("version", None)
            if isinstance(v, str) and name.lower().replace("-", "_") == d.lower().replace("-", "_"):
                parsed_version = _parse_version_dependency(v)
                if parsed_version:
                    operator, current_version = parsed_version
                    if not current_version or not latest_version:
                        continue
                    if LooseVersion(current_version) < LooseVersion(latest_version):  # Use LooseVersion
                        updated_version_str = f"{operator}{latest_version}"

                        def _replace_version(line):
                            if d in line and "<<SKIP_UPDATE>>" not in line:
                                line = line.replace(current_version, latest_version)
                            return line

                        content_lines = list(map(_replace_version, content_lines))
                        print(f"Updating {name} from {v} to {updated_version_str}")
                        deps[d] = updated_version_str
        return "\n".join(content_lines)

    for key in t["tool"]["poetry"].keys():
        if key.endswith("dependencies"):
            c = update(t["tool"]["poetry"][key], c.split("\n"))

    return c


@cli.command("update")
def update_deps() -> None:
    """Update dependencies to latest version.

    Note: This method is curretly in alpha... check the updated lines after calling it.
    TODO: Add the feature for soft update (highest and lowest possible version)
    """
    content = pathlib.Path("./pyproject.toml").read_text()
    toml_dict = cast(Dict, toml.loads(content))
    subprocess.run(["poetry", "update"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    output = subprocess.run(["pip", "list"], capture_output=True)
    lines = cast(str, output.stdout.decode()).split("\n")
    for line in filter(lambda x: bool(x), lines):
        module_vals = line.split()
        if len(module_vals) != 2:
            continue
        name, latest_version = module_vals
        content = _update_deps(name, latest_version, toml_dict, content)

    if content:
        with open("./pyproject.toml", "w") as fw:
            fw.write(content)

    subprocess.run(["poetry", "lock"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("Dependencies updated and pyproject.toml overwritten.")


if __name__ == "__main__":
    cli.main(["update"])
