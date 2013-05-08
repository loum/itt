PY=/usr/bin/env python
PYTHONPATH=../..
LOG_CONF=conf
NOSE=/usr/bin/nosetests -s -v

# The TEST variable can be set to allow you to control which tests
# to run.  For example, if the current project has a test set defined at
# "tests/test_<name>.py".  To run the "Test<class_name>" class:
#
# $ make test TEST=tests:Test<class_name>
#
# To run individual test cases within each test class:
#
# $ make test TEST=tests:Test<class_name>.test_<test_name>
#
# Note: for this to work you will need to import the test class into
# the current namespace via "tests/__init__.py"
TEST=

sdist:
	$(PY) setup.py sdist

docs:
	PYTHONPATH=$(PYTHONPATH) sphinx-build -b html ./doc/source ./doc/build

test:
	PYTHONPATH=$(PYTHONPATH) LOG_CONF=$(LOG_CONF) $(NOSE) $(TEST)

clean:
	git clean -xdf
