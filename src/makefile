.PHONY: clean

NAME 	   	:= Sistema de Recuperación de Información
VERSION	    := 1.0
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
	pip3 install bs4
	pip3 install math
	pip3 install nltk
	pip3 install numpy
	pip3 install collections

clean: ## Remove temporary files
	rm -rf cisi/__pycache__/
	rm -rf cranfield/__pycache__/
	rm -rf printer/__pycache__/
	rm -rf utils/__pycache__/

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
