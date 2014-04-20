default: test

clean:
	rm -f $(shell find . -name "*.pyc")

tests:
	nosetests

test_watcher:
	watch nosetests
