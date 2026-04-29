VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

install: requirements.txt
	@clear
	@python3 -m venv $(VENV)
	@$(PIP) install -r requirements.txt

run: install
	@. $(VENV)/bin/activate
	@clear
	@$(PYTHON) a_maze_ing.py default_config.txt

debug: install
	@. $(VENV)/bin/activate
	@clear
	@$(PYTHON) -m pdb ./a_maze_ing.py default_config.txt

lint:
	@echo "\033[35mflake8\033[0m"
	@flake8 . --exclude .venv
	@echo "\033[35mmypy\033[0m"
	@mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs . --exclude '.venv/'

lint-strict:
	@echo "\033[35mflake8\033[0m"
	@flake8 . --exclude .venv
	@echo "\033[35mmypy\033[0m"
	@mypy --strict . --exclude .venv

clean:
	@rm -rf ./src/configuration/conf_scripts/__pycache__
	@rm -rf ./src/__pycache__
	@rm -rf ./src/configuration/__pycache__
	@rm -rf $(VENV)
	@rm -rf ./custom_config.txt
	@rm -rf output.txt

.PHONY: run clean
