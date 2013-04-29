__all_ = [
    "Client",
]

from abc import ABCMeta, abstractmethod

from itt.utils.log import class_logging

import itt


@class_logging
class Client(object):
    """IP Test Tool generic client class.

    Through the `download` and `upload` methods, the Client class allows
    interaction with server infrastructure.

    """
    __metaclass__ = ABCMeta

    def __init__(self, config):
        """Client class initialisation.
        """
        self._client = None

        self.config = config

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, value):
        self._client = value

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        ##  Expect an itt.TestConfig object for config
        if type(value) is not itt.TestConfig:
            ##  XXX: Throw an ITT exception properly
            msg = "Expected an itt.TestConfig object for 'config'"
            log.error(msg)
            raise Exception(msg)
        else:
            self._config = value

    @abstractmethod
    def download(self, remotename, localname=None): pass

    @abstractmethod
    def upload(self, localname, remotename=None): pass

