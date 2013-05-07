""":mod:`itt.test.content` defines content that make up a ITT test case.
"""

__all__ = [
    "TestContent",
]

from itt.utils.log import class_logging


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

        Property getter/setter that defines the nature in which the
        content is generated.  If ``True``, the content is taken from a
        static source and guarantees consistency across invocations.  If
        ``False``, the content is generated randomly.

    """
    def __init__(self,
                 filename,
                 static=True):
        """
        """
        self._static = static

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value):
        self._filename = value

    @property
    def static(self):
        return self._static

    @static.setter
    def static(self, value):
        self._static = value
