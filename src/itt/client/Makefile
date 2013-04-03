PY=/usr/bin/env python
PYTHONPATH=..
LOG_CONF="../utils/conf"

sdist:
	$(PY) setup.py sdist

test:
	PYTHONPATH=$(PYTHONPATH) LOG_CONF=$(LOG_CONF) nosetests -s -v

clean:
	find . -type f -name "*.pyc" -exec rm {} \;
	rm -fr MANIFEST dist/ build/
