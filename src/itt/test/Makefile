PY=/usr/bin/env python
PYTHONPATH=../..:../../itt/control
LOG_CONF="../utils/conf"
DJANGO_SETTINGS_MODULE=itt.control.settings
TEST=

#sdist:
#	$(PY) setup.py sdist

#docs:
#	PYTHONPATH=$(PYTHONPATH) sphinx-build -b html ./doc/source ./doc/build

test:
	PYTHONPATH=$(PYTHONPATH) \
	DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS_MODULE) \
	LOG_CONF=$(LOG_CONF) \
	nosetests -s -v	$(TEST)

clean:
	find . -type f -name "*.pyc" -exec rm {} \;
	rm -fr MANIFEST dist/ build/
