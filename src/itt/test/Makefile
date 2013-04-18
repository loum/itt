PY=/usr/bin/env python
PYTHONPATH=../..
LOG_CONF="../utils/conf"

sdist:
	$(PY) setup.py sdist

docs:
	PYTHONPATH=$(PYTHONPATH) sphinx-build -b html ./doc/source ./doc/build

test:

	PYTHONPATH=$(PYTHONPATH) LOG_CONF=$(LOG_CONF) \
	nosetests -s -v ${TEST_FILE}

clean:
	find . -type f -name "*.pyc" -exec rm {} \;
	rm -fr MANIFEST dist/ build/
