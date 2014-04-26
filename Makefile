default: tests

clean:
	rm -f $(shell find . -name "*.pyc")

tests:
	python -m nose

test_watcher:
	watch python -m nose

style_check:
	python -m pep8 $(shell find . -name "*.py")

style_watcher:
	watch python -m pep8 $(shell find . -name "*.py")

lint_check:
	python -m pylint --report=n $(shell find . -name "*.py")
