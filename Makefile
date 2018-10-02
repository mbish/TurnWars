default: tests

clean:
	rm -f $(shell find . -name "*.pyc")

test: tests
tests: 
	python -m nose --with-coverage --cover-package game

test_watcher:
	watch python -m nose

style_check:
	python -m pep8 $(shell find . -name "*.py")

style_watcher:
	watch python -m pep8 $(shell find . -name "*.py")

lint_check:
	python -m pylint --report=n $(shell find . -name "*.py")

client: 
	python game/client/client.py

server: 
	python app.py

deps:
	pip install -r requirements.txt
