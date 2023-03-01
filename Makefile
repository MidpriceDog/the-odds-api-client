SHELL := $(shell which bash) # Use bash instead of bin/sh as shell
SYS_PYTHON := $(shell which python3 || echo ".python_is_missing")

ifndef VIRTUAL_ENV
VENV := .venv # Create a virtual environment if not in one
else
VENV := $(VIRTUAL_ENV) # Use current virtual environment if in one
endif

PIP := $(VENV)/bin/pip
TEST_FILE := tests/test.py
PYTHON := python3
OUTPUT_NAME?=theoddsapi
.DEFAULT_GOAL := help # Default target

.PHONY: help
help:
	@echo "make test [args] - Run unit tests. Args is an optional space delimited list of one or more of the test suites: sports, odds, event_odds, historical_odds, scores, usage_quota. If no arguments are supplied, all test suites are run."
	@echo "make install - Install necessary dependencies to use methods in the TheOddsAPI module. To be run after cloning git repo.
	@echo "make clean - Remove any built artifacts and cached files"
	@echo "make dist - Build .tar files"

.PHONY: test
test:
	$(PYTHON) $(TEST_FILE) $(TEST_ARGS) $(filter-out $@,$(MAKECMDGOALS))

# Allow passing arguments to the tests target
%:
	@echo ""

.PHONY: dist
dist:
	$(PYTHON) -m build

# For ease of upload to TestPyPI
.PHONY: testpypi
testpypi: 
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install --upgrade twine
	$(PYTHON) -m twine upload --repository testpypi dist/*

# For ease of upload to PyPI
.PHONY: pypi
pypi:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install --upgrade twine
	$(PYTHON) -m twine upload dist/*

.PHONY: install
install:
	@echo "Installing requirements..."
	$(PIP) install -r requirements.txt

.PHONY: clean
clean:
	@echo "Cleaning up..."
	rm -rf $(VENV) dist *.egg-info .mypy_cache .pytest_cache .cache
	find . -name '__pycache__' -exec rm -rf {} +

