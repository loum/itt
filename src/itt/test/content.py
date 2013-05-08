""":mod:`itt.test.content` defines content that make up a ITT test case.
"""

__all__ = [
    "TestContent",
]

from itt.utils.log import class_logging
from itt.utils.typer import (bool_check,
                             int_check,
                             float_check,
                             not_none_check)

import os


@class_logging
class TestContent(object):
    """Test content initialisation.

    .. note::

        All public attribute access is implemented in a Pythonic property
        decorator style.

    .. attribute:: filename

        Property getter/setter that defines whether the test content
        resource is file based or dynamic.  A *filename* not equal to
        ``None`` implies a file-based resource with the *filename* value
        assuming the name of the file.

    .. attribute:: static

        Property getter that defines the nature in which the
        content is generated.  If ``True``, the content is taken from a
        static source and guarantees consistency across invocations.  If
        ``False``, the content is generated randomly.

    .. attribute:: bytes

        Property getter/setter that defines the size of the content in
        bytes.  The setter is only valid for random data (that is, if 
        *filename* is ``None``).

    """
    def __init__(self,
                 filename,
                 bytes=None,
                ):
        """
        """
        self.filename = filename

        ##  Avoids typer.py throwing "TypeError: expecting a int value
        if bytes is not None:
            self.bytes = int(bytes)
        else:
            self._bytes = None

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value):
        self._filename = value

    @property
    def static(self):
        return self.filename is not None

    @property
    def bytes(self):
        ##  If it's a real file (not random data) then, check file for
        ##  up-to-date size
        if self.static:
            self._bytes = int(os.path.getsize(self.filename))

        return self._bytes

    @bytes.setter
    @int_check(greater_than=0)
    def bytes(self, value):
        ##  Only set if we're using random data
        if not self.static:
            self._bytes = value

    def open(self):
        """Opens the file (does nothing on a random data stream)."""

        if self.static:
            self._file = open(self.filename, "rb")

    def read(self):
        """Reads & returns the file from the current cursor position to
        ``EOF``, or if the content is a random data stream then return
        *self.bytes* of random data.
        """

        if self.static:
            return self._file.read()
        else:
            return os.urandom(self.bytes)

    def read(self, bytes):
        """Reads & returns *bytes* of data from the file from the
        current cursor position (unless ``EOF`` is reached first), or
        if the content is a random data stream then return *bytes* of
        random data.

        **Args:**

            bytes (int): Amount of data to return (unless ``EOF`` reached)
        """

        if self.static:
            return self._file.read(bytes)
        else:
            return os.urandom(bytes)

    def close(self):
        """Closes the file (does nothing on a random data stream)."""

        if self.static:
            self._file.close()
