.PHONY: help install update test coveralls lint black mypy run safety run-dev

help: ## Print this message
	@awk 'BEGIN { FS = ":.*##"; print "Usage:  make <target>\n\nTargets:" } \
	/^[-_[:alpha:]]+:.?*##/ { printf "  %-15s%s\n", $$1, $$2 }' $(MAKEFILE_LIST)

## ---- Dependency commands ---- ##

install: ## install dependencies
	pipenv install --dev

update: install ## update all Python dependencies
	pipenv clean
	pipenv update --dev

## ---- Unit test commands ---- ##

test: ## run tests and print a coverage report
	FLASK_ENV=testing pipenv run coverage run --source=cdnauth -m pytest -vv
	pipenv run coverage report -m
	pipenv run coverage html

coveralls: test
	pipenv run coverage lcov -o ./coverage/lcov.info

## ---- Code quality and safety commands ---- ##

# linting commands
lint: black ruff safety ## run all linters

black:
	pipenv run black --check --diff .

black-apply: # apply changes with 'black'
	pipenv run black .

ruff:
	pipenv run ruff check .

ruff-apply: # resolve 'fixable errors' with 'ruff'
	pipenv run ruff check --fix .

safety:
	pipenv check
	pipenv verify


## ---- Run the flask app (intended for development) ---- ##

run-dev: ## run the flask app in dev
	FLASK_ENV=development pipenv run flask --app cdnauth run --debug
	# example of how to use SSL in dev. Very useful if you override /etc/hosts to have localhost
	# act as touchstone registered SP
	# FLASK_ENV=development pipenv run flask --app cdnauth run --debug --cert=adhoc


run-prod: ## run the flask app in a prod-like mode
	FLASK_ENV=production pipenv run gunicorn --bind 0.0.0.0 cdnauth:app  --log-level debug --log-file -


## ---- Useful commands for managing the app when using a container for dev ---- ##

build: ## build local container
	docker build -t cdnauth-local .

app-bash: build ## bash shell in app container with linked file system to local directory
	docker run -it -v.:/app -p 5000:5000 -p 8000:8000 --env-file .env cdnauth-local bash
	# example of how to use SSL in dev. Very useful if you override /etc/hosts to have localhost
	# act as touchstone registered SP
	# docker run -it -v.:/app -p 443:5000 --env-file .env cdnauth-local bash
