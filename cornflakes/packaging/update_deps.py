import subprocess
from typing import Dict, cast

from packaging import version
import toml

from cornflakes.cli import cli


def _update_deps(name: str, latest_version: str, t: Dict, c: str) -> str:
    def update(deps: Dict, content: str) -> str:
        for key in deps:
            v = deps[key]
            if isinstance(v, str) and name.lower() == key.lower() and v[0] in ("~", "^"):
                current_version = v[1:]
                if version.parse(current_version) < version.parse(latest_version):
                    updated_version_str = f"{v[0]}{latest_version}"
                    content = content.replace(current_version, latest_version)
                    print(f"Updating {name} from {v} to {updated_version_str}")
                    deps[key] = updated_version_str
        return content

    c = update(t["tool"]["poetry"]["dependencies"], c)
    c = update(t["tool"]["poetry"]["dev-dependencies"], c)

    return c


@cli.command("update")
def update_deps() -> None:
    """Update dependencies to latest version."""
    with open("./pyproject.toml") as fr:
        content = fr.read()
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
    update_deps()
