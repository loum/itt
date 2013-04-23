PY=/usr/bin/env python
PYTHONPATH=.:../..
LOG_CONF=../utils/conf
DJANGO_INIT=./manage.py syncdb --noinput
DJANGO_CLEAN=./manage.py flush --noinput
DJANGO_TEST=./manage.py test
DJANGO_SETTINGS_MODULE=settings
TEST=

# Set up the target test files.
# I've moved the tests from the "preferred" Django location and into
# "<project>/<app>/tests/test_<name>.py" file to be more consistent with
# the ITT project.  Of course, the Django test runner does not like this.
# However, problem can be resolved by making an import call within
# __init__.py.  For example, if I have a test called
# "<project>/<app>/tests/test_x.py"
#
# edit <project>/<app>/tests/__init__.py
#
# from test_x import <test_class>
#
# With this construct, you can target individual test classes or test
# methods as follows:
#
# Test classes:
# ./manage.py test <app>.<test_class>
#
# Test class methods:
# ./manage.py test <app>.<test_class>.<test_class_method>

#sdist:
#	$(PY) setup.py sdist

docs:
	PYTHONPATH=$(PYTHONPATH) \
	DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS_MODULE) \
	sphinx-build -b html ./doc/source ./doc/build

init:
	$(PY) $(DJANGO_INIT)

test: django_test

clean:
	find . -type f -name "*.pyc" -exec rm {} \;
	$(PY) $(DJANGO_CLEAN)

django_test:
	PYTHONPATH=$(PYTHONPATH) LOG_CONF=$(LOG_CONF) \
	$(DJANGO_TEST) --verbosity=2 $(TEST)
