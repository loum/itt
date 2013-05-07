""":mod:`itt.test.content` defines content that make up a ITT test case.
"""

__all__ = [
    "TestContent",
]

from itt.utils.log import class_logging

import os


@class_logging
class TestContent(object):
    """Test content initialisation.

    .. note::

        All public attribute access is implemented in a Pythonic property
        decorator style.

    .. attribute: filename

        Property getter/setter that defines whether the test content
        resource is file based or dynamic.  A *filename* not equal to
        ``None`` implies a file-based resource with the *filename* value
        assuming the name of the file.

    .. attribute: static

        Property getter that defines the nature in which the
        content is generated.  If ``True``, the content is taken from a
        static source and guarantees consistency across invocations.  If
        ``False``, the content is generated randomly.

    .. attribute: bytes

        Property getter/setter that defines the size of the content in
        bytes.  The setter is only valid for random data (that is, if 
        *filename* is ``None``).

    """
    def __init__(self,
                 filename,
                ):
        """
        """
        self.filename = filename

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
        if self.static:
            ##  Check file for up-to-date size
            self._bytes = int(os.path.getsize(self.filename))

        return self._bytes

    @bytes.setter
    def bytes(self, value):
        if not self.static:
            self._bytes = value
