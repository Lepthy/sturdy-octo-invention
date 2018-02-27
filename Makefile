CWD = $(CURDIR)

PROJECT_NAME = crawler
PROJECT_HOME = $(CWD)

PROJECT_VENV = $(PROJECT_HOME)/.venv
PROJECT_CODE = $(PROJECT_HOME)/src
PROJECT_TEST = $(PROJECT_HOME)/tests


setup:
	@python3 -m venv ${PROJECT_VENV}
	@${PROJECT_VENV}/bin/pip install -r requirements.txt

setup-tests:
	@python3 -m venv ${PROJECT_VENV}
	@PYTHONPATH=${PROJECT_CODE} ${PROJECT_VENV}/bin/pip install -r requirements_tests.txt

unit:
	@echo "Running unit tests for $(PROJECT_TEST)/unit..."
	@${PROJECT_VENV}/bin/nosetests -s --tests=$(PROJECT_TEST)/unit --with-xunit

tests: unit

clean:
	@echo "Cleaning up *.pyc, *.sw[a-z] and *~ files"
	@find . -name "*.pyc" -delete
	@find . -name "*.sw[a-z]" -delete
	@find . -name "*~" -delete

fclean:
	@echo "Cleaning artifacts"
	@git clean -i -X -d

build: tests
	@docker build -t crawler .

.PHONY: build tests unit setup setup-tests fclean clean