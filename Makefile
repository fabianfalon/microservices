#!/usr/bin/make -f
PROJECT_NAME := 'Microservices'
.DEFAULT_GOAL := help

.PHONY: test build migrate
.PHONY: flake8 clean

test: ## Run test suite in project's main container
	docker-compose exec places python manage.py test
	docker-compose exec peoples python manage.py test

build: ## Build project image
	docker-compose build

migrate: ## Execute all migrations in project's main container
	docker-compose exec places python manage.py recreate_db
	docker-compose exec peoples python manage.py recreate_db
	docker-compose exec places python manage.py populate_db
	docker-compose exec peoples python manage.py populate_db

flake8: ## Run flake8
	docker-compose run --rm places flake8
	docker-compose run --rm peoples flake8

clean: ## Remove all .pyc
	find . -name "*.pyc" -exec rm -f {} \;
	find . -name '__pycache__' -exec rm -fr {} +

help: ## Display this help text
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'