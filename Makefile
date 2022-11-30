# Define locations of critical directories
APP_NAME=nebula
STATIC_SOURCE=$(APP_NAME)/static

# Arguments to external tools
# PY_FILES=$(APP_NAME)/*.py $(APP_NAME)/**/*.py *.py
BLACK_ARGS=
ISORT_ARGS=--multi-line=3 --trailing-comma --force-grid-wrap=0 --use-parentheses
FLAKE_ARGS=

# Arguments for flask
FLASK_APP=$(APP_NAME)
FLASK_ENV_DEV=development
DEV_ENV=FLASK_DEBUG=1 FLASK_APP=$(FLASK_APP) FLASK_ENV=$(FLASK_ENV_DEV)

# List all scss files in the nebula/static/scss directory & create a : separated list from them
SCSS_FILES=$(shell find ./nebula/static/scss -name '*.scss' | xargs echo | sed 's/ /:/g')


default: help


## Running and Installing
dev-server:  ## Start the development version of the website
	FLASK_RUN_EXTRA_FILES="$(SCSS_FILES)" $(DEV_ENV) flask run

install: check-in-venv ## Installs the flask app (siriusaweb) in the environment
	python3 setup.py sdist bdist_wheel
	pip install dist/$(APP_NAME)-*.tar.gz


## Database stuff
db-migrate-fresh:  ## Remove current database & initialize fresh database
	-rm -f nebula/site.db
	touch nebula/site.db
	pip install -e .
	python3 database-setup/db_init.py

db-seed:  ## Populate the database with test data
	python3 database-setup/db_seed.py

db-migrate-fresh-seed: db-migrate-fresh db-seed  ## Reload and seed

compile-sass:  ## Compile SCSS files into CSS files
	npx sass --update $(STATIC_SOURCE)/scss:$(STATIC_SOURCE)/css


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
deps_dev: deps_pkg  ## Install development dependencies
	#pip install -r requirements.dev.txt

deps_js:  ## Install javascript dependencies
	npm install

deps_pkg: deps_misc deps_js  ## Install package dependencies
	pip install -r requirements.txt

deps_misc: ## Install dependencies not in the requirement file, but still required for package management
	pip install wheel


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
