__all_ = [
    "Client",
]

from abc import ABCMeta, abstractmethod

from itt.utils.log import log, class_logging

import itt


@class_logging
class Client(object):
    """IP Test Tool generic client class.

    Through the `download` and `upload` methods, the Client class allows
    interaction with server infrastructure.

    """
    __metaclass__ = ABCMeta

    def __init__(self, test=None):
        """Client class initialisation.
        """
        self._client = None

        self.test = test

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, value):
        self._client = value

    @property
    def test(self):
        return self._test

    @test.setter
    def test(self, value):
        self._test = value

    @abstractmethod
    def download(self): pass

    @abstractmethod
    def upload(self): pass

