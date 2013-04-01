PY=/usr/bin/env python
PYTHONPATH=..
LOG_CONF="conf"

sdist:
	$(PY) setup.py sdist

test:
	#PYTHONPATH=$(PYTHONPATH) nosetests -s -v
	PYTHONPATH=$(PYTHONPATH) LOG_CONF=$(LOG_CONF) nosetests -s -v

clean:
	find . -type f -name "*.pyc" -exec rm {} \;
	rm -fr MANIFEST dist/ build/
