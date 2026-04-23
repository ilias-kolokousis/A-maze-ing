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
	@$(PYTHON) ./src/a_maze_ing.py

debug: install
	@. $(VENV)/bin/activate
	@clear
	@$(PYTHON) -m pdb ./src/a_maze_ing.py

lint: install
	flake8 
	mypy --warn-return-any

clean:
	@rm -rf ./src/configuration/conf_scripts/__pycache__
	@rm -rf ./src/configuration/__pycache__
	@rm -rf $(VENV)
	@rm -rf ./src/custom_config.ini

.PHONY: run clean
