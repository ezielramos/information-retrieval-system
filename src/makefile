.PHONY: clean

NAME 	   	:= Sistema de Recuperación de Información
VERSION		:= 1.0
DEVELOPERS	:= Thalia Blanco, Eziel Ramos, Ariel Plasencia
COPYRIGHT  	:= Copyright © 2022: $(DEVELOPERS)

main: ## Compiling the project :)
	@echo "Compiling the project :)"

run: ## Run the project ;)
	python3 main.py

info: ## Display project description
	@echo "$(NAME) v$(VERSION)"
	@echo "$(COPYRIGHT)"

version: ## Show the project version
	@echo "$(NAME) v$(VERSION)"

install: ## Install the project dependencies
	pip3 install nltk

clean: ## Remove temporary files
	rm -rf tools/__pycache__/
	rm -rf evaluation_system/__pycache__/

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
