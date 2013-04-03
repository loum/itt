__all__ = [
    "Server",
]

from abc import ABCMeta, abstractmethod

"""
:mod:`server` --- IP Test Tool abstract base server class
=========================================================

.. module:: server
    :synopsis: IP Test Tool abstract base server class.

Base server class that provides a consistent interface across all server
variants.

The `thread` module templates the following public methods and attributes:

    .. note::

        All public attribute access is implemented in a Pythonic property
        decorator style.

.. attribute:: port

    The port that the server process should bind to.

.. attribute:: root

    The directory structure that the server will server files to/from.

.. attribute:: proc

    Handle to the :mod:`multiprocessing` object.

.. attribute:: daemon

    Hmmm, not sure we need this attribute at the class level.  Probably
    better defined in the control script -- caveat emptor as it may
    disappear soon.

.. attribute:: server

    The intention behind the `server` attribute is to provide a common
    access point to functionality provided via an alternate server-type
    module.  For example, somewhere in the IP Test Tool :class:`TftpServer`
    class is the following call:

        self.server = tftpy.TftpServer(self.root)

    This give us access to the nice features of the :mod:`tftp` module
    that we can then use in our own :meth:`start` and :meth:`stop` methods.

.. attribute:: bind

    Name of the host address.  Defaults to `localhost`.

.. attribute:: pid

    The PID of the server process.  A value of ``None`` indicates an
    inactive server.
"""

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
        self._bind = 'localhost'
        self._pid = None

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

    @bind.setter
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

    @abstractmethod
    def start(self): pass

    @abstractmethod
    def stop(self): pass
