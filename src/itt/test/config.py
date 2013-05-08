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

    .. attribute:: upload

        ``bool`` value which flags the test case for upload (from the
        perspective of the client).  Defaults to ``False``.

    .. attribute:: minimum_gap

        Defines the minimum gap between chunks of data, in seconds.
        Only valid if chunk_size is not ``None``.

    .. attribute:: chunk_size

        Defines the amount of data that will be sent 'at full speed',
        before having an optional gap (as defined by *minimum_gap*).
    """

    def __init__(self,
                 upload=False,
                 minimum_gap=None,
                 chunk_size=None,
    ):
        ##  properties
        self.upload = upload
        self.minimum_gap = minimum_gap
        self.chunk_size = chunk_size

    def __repr__(self):
        return "<TestConfig upload:%s minimum_gap:%s chunk_size:%s>" % (
            self.upload,
            self.minimum_gap,
            self.chunk_size,
        )

    ##--upload
    @property
    def upload(self):
        return self._upload

    @upload.setter
    @bool_check
    def upload(self, value):
        self._upload = value

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
