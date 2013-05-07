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

    .. attribute: generation

    """
    def __init__(self,
                 generation=None):
        """
        """
        print('inside TestContent __init__')
