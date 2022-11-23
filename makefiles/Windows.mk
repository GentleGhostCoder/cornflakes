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
	if exist build rd /s /q build
	if exist build rd /s /q dist
	if exist build rd /s /q .eggs
	if exist build rd /s /q cmake-build-debug
	if exist build rd /s /q inst/_cornflakes/cmake-build-debug
	for /d /r . %%d in (*.egg-info) do @if exist "%%d" echo "%%d" && rd /s/q "%%d"
	del /q /s /f .\*.egg


clean-pyc: ## remove Python file artifacts
	del /s /f /q .\*.pyc
	del /s /f /q .\*.pyo
	del /s /f /q .\*~
	for /d /r . %%d in (*__pycache__) do @if exist "%%d" echo "%%d" && rd /s/q "%%d"

clean-test: ## remove test and coverage artifacts
	if exist .tox rd /s /q .tox
	if exist .coverage rd /s /q .coverage
	if exist htmlcov rd /s /q htmlcov
	if exist .pytest_cache rd /s /q .pytest_cache

lint: ## check style with flake8
	flake8 cornflakes tests

test: ## run tests quickly with the default Python
	pytest

test-all: ## run tests on every Python version with tox
	tox

coverage: ## check code coverage quickly with the default Python
	coverage run --source cornflakes -m pytest
	coverage report -m
	coverage html
	$(BROWSER) htmlcov\index.html

docs: ## generate Sphinx HTML documentation, including API docs
	del /f /q docs\cornflakes.rst
	del /f /q docs\modules.rst
	del /f /q docs/_generated
	del /f /q docs/_build
	del /f /q docs/cornflakes*.rst
	sphinx-apidoc -o docs cornflakes
	$(MAKE) -C docs clean
	$(MAKE) -C docs html

preview: docs
	$(BROWSER) docs\_build\html\index.html

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

bump:
	poetry version $(git describe --tags --abbrev=0)

publish: dist ## package and upload a release
	poetry publish

dist: clean-build clean-pyc ## builds source and wheel package
	poetry build

install: clean-build clean-pyc dist ## install the package to the active Python's site-packages
	# pip install dist/*.whl
	poetry install --verbose # not working for some reason
