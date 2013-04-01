PY=/usr/bin/env python
PYTHONPATH=.

sdist:
	$(PY) setup.py sdist

test:
	PYTHONPATH=$(PYTHONPATH) nosetests -s -v

clean:
	find . -type f -name "*.pyc" -exec rm {} \;
	rm -fr MANIFEST dist/ build/
