## <img src="https://github.com/semmjon/cornflakes/blob/main/assets/cornflakes.png?raw=true" alt="cornflakes logo" width="400" height="400"/>

![PyPI](https://img.shields.io/pypi/v/cornflakes.svg)
![Python Version](https://img.shields.io/pypi/pyversions/cornflakes)
![License](https://img.shields.io/github/license/semmjon/cornflakes)
![Read the Docs](https://github.com/sgeist-ionos/cornflakes/actions/workflows/build_package.yml/badge.svg?branch=main)
![Build](https://github.com/semmjon/cornflakes/workflows/Build%20cornflakes%20Package/badge.svg)
![Tests](https://github.com/sgeist-ionos/cornflakes/actions/workflows/run_tests.yml/badge.svg?branch=main)
![Codecov](https://codecov.io/gh/sgeist-ionos/cornflakes/graph/badge.svg?token=FY72EIXI82)

```bash
pip install cornflakes
```

```bash
pip install git+https://github.com/semmjon/cornflakes
```

> :warning: **Warning**: Please be careful when using this Python module. Currently, it is only developed / tested by me, which is why it has a high update / change rate. I'm actually trying to be compatible with implementations, but I can't guarantee this at the moment. The module is currently still in a beta state and is not recommended for productive use.

---

## Information

The Python module "cornflakes" was started as a hobby project and offers an alternative to Pydantic for managing configurations and data structures. It allows creating generic and easy to manage configurations for your project. Unlike Pydantic, which is based on inheritance, "cornflakes" uses a decorator (similar to dataclass) to map data structures.

### Short Term RoadMap

-   Add autocompletion support for click CLI (automatically)
-   Change Code Annotations
    -   remove Any annotations if possible
    -   change Protocol Annotations to specific type classes
-   Enrich json methods
-   Fix / Test the to\_<file-format> Methods (specially yaml)

---

## Development

### Prerequisites

-   A compiler with C++17 support
-   Pip 10+ or CMake >= 3.4
-   Python 3.8+
-   doxygen
-   cppcheck
-   clang-tools-extra or clang-tidy

### Commands

Clone this repository and pip install. Note the `--recursive` option which is needed for the pybind11 submodule:

```bash
git clone --recursive https://gitlab.blubblub.tech/sgeist/cornflakes.git
```

Install the package using makefiles:

```bash
make install
```

Build dist using makefiles:

```bash
make dist
```

Run tests (pytest) using makefiles:

```bash
make test
```

Run all tests using makefiles:

```bash
make test-all
```

Run lint using makefiles:

```bash
make lint
```

Create dev venv:

```bash
python -m venv .venv
source .venv/bin/activate
pip install ninja pre-commit poetry
```

Install pre-commit:

```bash
pre-commit install
```

Update pre-commit:

```bash
pre-commit update -a
```

Run pre-commit:

```bash
pre-commit run -a
```
