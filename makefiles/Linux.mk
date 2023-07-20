.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr '*.so'
	rm -fr build/
	rm -fr setup.py
	rm -fr dist/
	rm -fr .eggs/
	rm -fr cmake-build-debug
	rm -fr inst/_cornflakes/cmake-build-debug
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

lint: ## check style with flake8
	flake8 cornflakes tests

test: ## run tests quickly with the default Python
	pytest -o log_cli=true

test-mypy:
	mypy cornflakes tests docs/conf.py

test-xdoctest:
	python -m xdoctest cornflakes all

test-pytype:
	pytype --disable=import-error cornflakes tests docs/conf.py

test-typeguard:
	 pytest --typeguard-packages=cornflakes

test-all: ## run tests on every Python version with tox
	nox

coverage: ## check code coverage quickly with the default Python
	coverage run --source cornflakes -m pytest
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/cornflakes.rst
	rm -f docs/modules.rst
	rm -rf docs/_generated
	rm -rf docs/_build
	rm -f docs/cornflakes*.rst
	sphinx-apidoc -o docs cornflakes
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

bump-patch:
	cornflakes bump "patch"

bump-minor:
	cornflakes bump "minor"

bump-major:
	cornflakes bump "major"

bump: bump-patch # default

update:
	cornflakes update

publish: dist ## package and upload a release
	poetry publish

dist: clean-build clean-pyc bump ## builds source and wheel package
	poetry build

install: clean-build clean-pyc ## install the package to the active Python's site-packages
	# pip install dist/*.whl
	poetry install --verbose # not working for some reason -> not copying source files

all: install dist
	c++ --version  # default compile method (not needed but here for the IDE)
