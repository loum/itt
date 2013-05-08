PY=/usr/bin/env python
PYTHONPATH=..
LOG_CONF=itt/utils/conf
NOSE=/usr/bin/nosetests -s -v
TEST=client server utils

sdist:
	$(PY) setup.py sdist

docs:
	PYTHONPATH=$(PYTHONPATH) sphinx-build -b html ./doc/source ./doc/build

test:
	PYTHONPATH=$(PYTHONPATH) LOG_CONF=$(LOG_CONF) $(NOSE) $(TEST)

clean:
	git clean -xdf

.PHONY: test clean
