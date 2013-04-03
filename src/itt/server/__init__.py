__all__ = [
    "Server",
]

from abc import ABCMeta, abstractmethod


class Server(object):
    """IP Test Tool generic server class.

    Class server is defined as "abstract" so that it forces generalisations
    to implement a consistent interface.  It is not intended to be
    instantiated directly.  This will hopefully simplify the
    client interactions to various server resources.

    """

    __metaclass__ = ABCMeta

    def __init__(self):
        """Server class initialisation.
        """
        self._port = None
        self._root = None
        self._proc = None
        self._daemon = None
        self._server = None

    @abstractmethod
    def start(self): pass

    @abstractmethod
    def stop(self): pass

    @property
    def port(self):
        return self._port

    @port.setter
    @abstractmethod
    def port(self, value):
        self._port = value

    @property
    def bind(self):
        return self._bind

    @port.setter
    @abstractmethod
    def bind(self, value):
        self._bind = value

    @property
    def root(self):
        return self._root

    @root.setter
    @abstractmethod
    def root(self, value):
        self._root = value

    @property
    def proc(self):
        return self._proc

    @proc.setter
    #@abstractmethod
    def proc(self, value):
        self._proc = value

    @property
    def daemon(self):
        return self._daemon

    @daemon.setter
    @abstractmethod
    def daemon(self, value):
        self._daemon = value

    @property
    def server(self):
        return self._server

    @server.setter
    @abstractmethod
    def server(self, value):
        self._server = value
