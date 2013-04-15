__all__ = [
    "Server",
]

from abc import ABCMeta, abstractmethod

import itt.utils


class Server(itt.utils.Daemon):
    """IP Test Tool base server class.

    :class:`Server` is built on top of the :mod:`abc` Abstract Base Class
    module and is defined as "abstract".  It is not intended to be
    instantiated directly.  Instead, it forces generalisations to 
    implement a consistent interface.  This will hopefully simplify the
    client interaction across various server resources.

    .. note::

        All public attribute access is implemented in a Pythonic property
        decorator style.

    .. attribute:: port

        The port that the server process should bind to.

    .. attribute:: root

        The directory structure that the server will server files to/from.

    .. attribute:: proc

        Handle to the :mod:`multiprocessing` object.

    .. attribute:: server

        The intention behind the `server` attribute is to provide a common
        access point to functionality provided via an alternate server-type
        module.  For example, somewhere in the IP Test Tool
        :class:`TftpServer` class is the following call:

            self.server = tftpy.TftpServer(self.root)

        This give us access to the nice features of the :mod:`tftp` module
        that we can then use in our own :meth:`start` and :meth:`stop`
        methods.

    .. attribute:: bind

        Name of the host address.  Defaults to `localhost`.

    .. attribute:: pid

        The PID of the server process.  A value of ``None`` indicates an
        inactive server.

    .. attribute:: pidfile (string)

        The name of the PID file.  Only required if intending to run as
        a daemon.  Defaults to ``None`` which suppresses daemonisation
        functionality.

#    .. attribute:: exit_event (:class:`multiprocessing.Event`)
#
#        Internal semaphore that when set, signals that the server process
#        is to be terminated.

    """
    __metaclass__ = ABCMeta

    def __init__(self, pidfile=None):
        """Server class initialisation.
        """
        super(Server, self).__init__(pidfile)

        self._port = None
        self._root = None
        self._proc = None
        self._server = None
        self._bind = 'localhost'
        self._pid = None
        self._pidfile = pidfile
        #self._exit_event = multiprocessing.Event()

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
    def server(self):
        return self._server

    @server.setter
    @abstractmethod
    def server(self, value):
        self._server = value

    @property
    def pidfile(self):
        return self._pidfile

    @pidfile.setter
    def pidfile(self, value):
        self._pidfile = value
