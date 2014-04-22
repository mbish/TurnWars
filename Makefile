default: test

clean:
	rm -f $(shell find . -name "*.pyc")

tests:
	nosetests

test_watcher:
	watch nosetests

style_check:
	pep8 $(shell find . -name "*.py")

style_watcher:
	watch pep8 $(shell find . -name "*.py")

lint_check:
	pylint --report=n $(shell find . -name "*.py")
