# Define locations of critical directories
SITE_DIR=/Public_html/users/sirius/site
APP_NAME=nebula
STATIC_DIR=$(SITE_DIR)/static
STATIC_SOURCE=$(APP_NAME)/static

# Arguments to external tools
PY_FILES=nebula/*.py nebula/views/*.py *.py 
BLACK_ARGS=-l 79
ISORT_ARGS=--multi-line=3 --trailing-comma --force-grid-wrap=0 --use-parentheses --line-width=79
FLAKE_ARGS=

# Arguments for flask
FLASK_APP=nebula
FLASK_ENV_DEV=development


## Run this by using `make` or `make server`
# Steps which are taken by this command:
# 1. Ensure the user is in a virtual environment
# 2. Install the flask app in the virtual environment using pip
# 3. Copy the contents in the app static directory, to the open static directory
# 4. Update the last modified timestamp on the wsgi file to restart server
# 5. Clean up files which are no longer needed.
# 6. Add write permissions to all group users
server: install copy-static update-wsgi clean update-group-permissions

# Quick version of 'server', it will not copy all the static content & permissions
quick-update: install update-wsgi clean

# Start/Start the development version of the website
# dev-server: SHELL := /bin/bash
# find all scss files and add them to the extra files that flask will watch
dev-server:
	@export search_dir="./nebula/static/scss"/* ; \
	export FLASK_RUN_EXTRA_FILES="" ; \
	\
	for i in $$(find $$search_dir -name "*.scss") ; \
	do  \
		export FLASK_RUN_EXTRA_FILES="$$FLASK_RUN_EXTRA_FILES$$i:" ; \
	done ; \
	export FLASK_RUN_EXTRA_FILES=$${FLASK_RUN_EXTRA_FILES%?} ; \
	\
	FLASK_RUN_EXTRA_FILES=$${FLASK_RUN_EXTRA_FILES} \
	FLASK_APP=$(FLASK_APP) \
	FLASK_ENV=$(FLASK_ENV_DEV) \
	flask run ;


# Installs the flask app (siriusaweb) in the environment
install: check-in-venv
	python3 setup.py sdist bdist_wheel
	pip install dist/$(APP_NAME)-*.tar.gz

copy-static:
	cp -r $(STATIC_SOURCE) $(SITE_DIR)

# Add write permissions to the group in the site directory 
# Currently pretty slow.
update-group-permissions:
	-chmod g+w -R $(SITE_DIR)/* $(SITE_DIR)/.env $(SITE_DIR)/.git $(SITE_DIR)/.gitignore

update-wsgi:
	touch $(SITE_DIR)/main.wsgi

# Will error and stop the pipeline if this check fails
check-in-venv:
	env | grep 'VIRTUAL_ENV'

# Cleans up some files made by python.
clean:
	-rm -rf $(APP_NAME).egg-info
	-rm -rf dist
	-rm -rf build

## Formatting and linting
format:
	black $(BLACK_ARGS) $(PY_FILES)
	isort $(ISORT_ARGS) $(PY_FILES)

check-format:
	black --check $(BLACK_ARGS) $(PY_FILES)
	isort --check-only $(ISORT_ARGS) $(PY_FILES)

lint:
	flake8 $(FLAKE_ARGS) $(PY_FILES)
