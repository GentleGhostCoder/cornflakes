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

test-types: test-mypy test-xdoctest test-typeguard test-pytype

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
	git pull
	cornflakes bump "patch"

bump-minor:
	git pull
	cornflakes bump "minor"

bump-major:
	git pull
	cornflakes bump "major"

bump: bump-patch # default

pr: bump
	@if [ -n "$$(git status --porcelain --ignore-submodules)" ]; then \
		echo "You have unstaged/committed changes. Please commit or stash them first."; \
		exit 1; \
	fi && \
	if [ -n "$$(git log @{u}..)" ]; then \
		echo "There are commits that haven't been pushed yet. Please push your changes first."; \
		exit 1; \
	fi && \
	BRANCH_NAME=$(shell git branch --show-current) && \
	gh pr create --base main --head $$BRANCH_NAME --title "PR $$BRANCH_NAME - $$(poetry version -s)" --body "$(filter-out $@,$(MAKECMDGOALS))"

pr-status:
	@BRANCH_NAME=$(shell git branch --show-current) && \
	COMMIT_HASH=$(shell git rev-parse HEAD) && \
	PR_NUMBER=$$(gh pr list --base $$BRANCH_NAME --json number -q ".[0].number") && \
	CHECK_RUNS=$$(gh api --paginate repos/:owner/:repo/commits/$$COMMIT_HASH/check-runs) && \
	SUCCESSFUL=$$(echo "$$CHECK_RUNS" | jq '[.check_runs[] | select(.status == "completed" and .conclusion == "success")] | length') && \
	IN_PROGRESS=$$(echo "$$CHECK_RUNS" | jq '[.check_runs[] | select(.status == "in_progress")] | length') && \
	QUEUED=$$(echo "$$CHECK_RUNS" | jq '[.check_runs[] | select(.status == "queued")] | length') && \
	echo "$$SUCCESSFUL successful, $$IN_PROGRESS in progress, and $$QUEUED queued checks" && \
	([ $$SUCCESSFUL -gt 0 ] && [ $$IN_PROGRESS -eq 0 ] && [ $$QUEUED -eq 0 ])


#🌈
pr-merge-if-ready: bump
	@if [ -n "$$(git status --porcelain --ignore-submodules)" ]; then \
		echo "You have unstaged/committed changes. Please commit or stash them first."; \
		exit 1; \
	fi && \
	if [ -n "$$(git log @{u}..)" ]; then \
		echo "There are commits that haven't been pushed yet. Please push your changes first."; \
		exit 1; \
	fi && \
	if $(MAKE) pr-status; then \
		BRANCH_NAME=$(shell git branch --show-current) && \
		PR_NUMBER=$$(gh pr list --base $$BRANCH_NAME --json number -q ".[0].number") && \
		gh pr merge $$PR_NUMBER --auto --merge; \
	else \
		echo "PR is not ready to be merged due to pending or failing checks."; \
	fi


release: pr-merge-if-ready
	@# Fetch the latest status of the main branch from the remote
	git fetch origin main:main && \
	OPEN_PRS_COUNT=$$(gh pr list --base main --state open --json number | jq ". | length") && \
    	if [ "$$OPEN_PRS_COUNT" -ne 0 ]; then \
    		echo "There are open PRs targeting the main branch. Resolve them before creating a tag."; \
    		exit 1; \
    	fi && \
	VERSION=$$(poetry version -s) && \
	echo "Detected version: $$VERSION" && \
	if git rev-parse "$$VERSION" >/dev/null 2>&1; then \
		echo "Tag $$VERSION already exists."; \
	else \
		echo "Creating new tag $$VERSION on the remote main branch." && \
		git tag "$$VERSION" origin/main && \
		git push origin "$$VERSION" && \
		gh release create "$$VERSION" --title "$$VERSION 🌈" --generate-notes; \
		echo "Tag $$VERSION has been created on the remote main branch and pushed. A new GitHub release has been made with title '$$VERSION 🌈'."; \
	fi


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
