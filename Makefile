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
	pipenv run coverage html

coveralls: test
	pipenv run coverage lcov -o ./coverage/lcov.info

## ---- Code quality and safety commands ---- ##

# linting commands
lint: black ruff safety ## run all linters

black:
	pipenv run black --check --diff .

ruff:
	pipenv run ruff check .

safety:
	pipenv check
	pipenv verify


## ---- Run the flask app (intended for development) ---- ##

run-dev: ## run the flask app in dev
	FLASK_ENV=development pipenv run flask --app cdnauth run --debug

run-prod: ## run the flask app in a prod-like mode
	FLASK_ENV=production pipenv run gunicorn --bind 0.0.0.0 cdnauth:app  --log-level debug --log-file -


## ---- Useful commands for managing the app when using a container for dev ---- ##

build: ## build local container
	docker build -t cdnauth-local .

app-bash: build ## bash shell in app container with linked file system to local directory
	docker run -it -v.:/app -p 5000:5000 -p 8000:8000 --env-file .env cdnauth-local bash
