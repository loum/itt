__all__ = [
    "Test",
]

from abc import ABCMeta, abstractmethod


class Test():
    """IP Test Tool base test class.

    I'm not sure exactly how I'll use this just yet.
    It might be abstract, or it might not.

    Loose idea at the moment:
    t = itt.Test(itt.test.config)
    t.execute()
    t.reportRestuls()
    """
    __metaclass__ = ABCMeta

    pass
