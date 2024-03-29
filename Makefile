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
	pipenv run coverage run --source=cdnauth -m pytest -vv
	pipenv run coverage report -m

coveralls: test
	pipenv run coverage lcov -o ./coverage/lcov.info

## ---- Code quality and safety commands ---- ##

# linting commands
lint: black mypy ruff safety ## run all linters

black:
	pipenv run black --check --diff .

mypy:
	pipenv run mypy .

ruff:
	pipenv run ruff check .

safety:
	pipenv check
	pipenv verify


## ---- Run the flask app (intended for development) ---- ##

run-dev: ## run the flask app in dev
	FLASK_ENV=development pipenv run flask --app cdnauth run --debug

run-prod: ## run the flask app in a prod-like mode
	FLASK_ENV=production pipenv run gunicorn cdnauth:app --log-file -
