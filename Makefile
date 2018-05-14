LINTER=pylint

default: tests

clean:
	rm -f $(shell find . -name "*.pyc")

tests: 
	python -m nose --with-coverage --cover-package game

test_watcher:
	watch python -m nose

style_check:
	python -m ${LINTER} $(shell find . -name "*.py")

style_watcher:
	watch -c make lint_check

lint_check:
	@python -m pylint -f json $(shell find . -name "*.py") | pylint-parser

client: 
	python game/client/client.py

server: 
	python app.py

deps:
	pip install -r requirements.txt
