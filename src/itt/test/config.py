""":mod:`itt.test.config` defines the settings that make up a ITT test case.
"""

__all__ = [
    "TestConfig",
]

from itt.utils.log import log, class_logging
from itt.utils.typer import (bool_check,
                             int_check,
                             float_check,
                             not_none_check)


@class_logging
class TestConfig(object):
    """Test Configuration...

    .. note::

        All public attribute access is implemented in a Pythonic property
        decorator style.

    .. attribute:: minimum_gap

        Defines the minimum gap between chunks of data, in seconds.
        Only valid if chunk_size is not ``None``.

    .. attribute:: chunk_size

        Defines the amount of data that will be sent 'at full speed',
        before having an optional gap (as defined by *minimum_gap*).
    """

    def __init__(self,
                 minimum_gap=None,
                 chunk_size=None,
    ):
        ##  properties
##  I'm having issues with typer.py not validating ints & floats correctly...
##  workaround below --pjay
        self.minimum_gap = None
        if minimum_gap is not None:
            self.minimum_gap = float(minimum_gap)

        self.chunk_size = None
        if chunk_size is not None:
            self.chunk_size = int(chunk_size)

    def __repr__(self):
        return "<TestConfig minimum_gap:%s chunk_size:%s>" % (
            self.minimum_gap,
            self.chunk_size,
        )

    ##--minimum_gap
    @property
    def minimum_gap(self):
        return self._minimum_gap

    @minimum_gap.setter
    @float_check(greater_than=0)
    def minimum_gap(self, value):
        self._minimum_gap = value

    ##--chunk_size
    @property
    def chunk_size(self):
        return self._chunk_size

    @chunk_size.setter
    @int_check(greater_than=0)
    def chunk_size(self, value):
        self._chunk_size = value
