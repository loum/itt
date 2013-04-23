PY=/usr/bin/env python
PYTHONPATH=..
LOG_CONF=itt/utils/conf
NOSE=/usr/bin/nosetests -s -v
TEST=client server utils

sdist:
	$(PY) setup.py sdist

test:
	PYTHONPATH=$(PYTHONPATH) LOG_CONF=$(LOG_CONF) $(NOSE) $(TEST)

clean:
	find . -type f -name "*.pyc" -exec rm {} \;
	rm -fr MANIFEST dist/ build/

.PHONY: test clean
