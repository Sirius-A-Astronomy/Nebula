# Define locations of critical directories
APP_NAME=nebula
STATIC_SOURCE=$(APP_NAME)/static

# Arguments to external tools
PY_FILES=$(shell find $(APP_NAME) tests -name '*.py' | xargs echo) *.py
BLACK_ARGS=
ISORT_ARGS=--multi-line=3 --trailing-comma --force-grid-wrap=0 --use-parentheses
FLAKE_ARGS=

# Arguments for flask
FLASK_APP=$(APP_NAME)
FLASK_ENV_DEV=development
DEV_ENV=FLASK_DEBUG=1 FLASK_APP=$(FLASK_APP) FLASK_ENV=$(FLASK_ENV_DEV)

default: help


## Running and Installing
dev-server:  ## Start the development version of the website
	$(DEV_ENV) flask run

prod-server:  ## Start the production version of the website
	FLASK_APP=$(FLASK_APP) flask run

install: check-in-venv ## Installs the flask app (siriusaweb) in the environment
	python3 setup.py sdist bdist_wheel
	pip install dist/$(APP_NAME)-*.tar.gz

build:
	npm run docs:build
	npm run build

## Formatting and linting
# TODO: Black, Isort & flake8 are not yet setup.
format:  ## Format the project (black & isort)
	black $(BLACK_ARGS) $(PY_FILES)
	isort $(ISORT_ARGS) $(PY_FILES)

check-format:  ## Check if the formatter is satisfied, error on an issue
	black --check $(BLACK_ARGS) $(PY_FILES)
	isort --check-only $(ISORT_ARGS) $(PY_FILES)

lint:  ## Run the linter (flake8)
	flake8 $(FLAKE_ARGS) $(PY_FILES)


## Testing
# TODO: Cypress tests do not work atm, since the dev-server needs to be running
test: test-py  ## Run all tests for the package

test-py:
	pytest
test-js:
	npx cypress run

## Dependencies
deps-dev: deps-pkg  ## Install development dependencies
	pip install -r requirements.dev.txt

deps-pkg: deps-misc deps-js  ## Install package dependencies
	pip install -r requirements.txt

deps-misc: ## Install dependencies not in the requirement file, but still required for package management
	pip install wheel
	pip install setuptools
	pip install pip-tools

deps-js:  ## Install javascript dependencies
	npm install

deps-upgrade:
	pip-compile requirements.in --upgrade
	pip-compile requirements.dev.in --upgrade

## Other
help: ## Prints help for targets with comments
	@cat $(MAKEFILE_LIST) | grep -E '^[a-zA-Z_-]+:.*?## .*$$' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

# Will error and stop the pipeline if this check fails
check-in-venv:  ## Check if the current shell is in a virtual environment
	env | grep 'VIRTUAL_ENV'

clean: ## Cleans up some files made by python.
	-rm -rf $(APP_NAME).egg-info
	-rm -rf dist
	-rm -rf build


# [SERVER STUFF]
server-update: check-in-venv deps-pkg build