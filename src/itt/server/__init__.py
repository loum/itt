__all__ = [
    "Server",
]

import multiprocessing
import time
from abc import ABCMeta, abstractmethod

import itt.utils
from itt.utils.log import log


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

    .. attribute:: exit_event (:class:`multiprocessing.Event`)

        Internal semaphore that when set, signals that the server process
        is to be terminated.

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
        self._exit_event = multiprocessing.Event()

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

    @property
    def exit_event(self):
        return self._exit_event

    @exit_event.setter
    def exit_event(self, value):
        self._exit_event = value

    #@abstractmethod
    def start(self):
        """.. method:: start

        Wrapper around the FTP server start process.

        Invokes the FTP server one in two ways:

        * As a daemon
        * Inline using the :mod:`multiprocessing.Event` module

        Typically, the daemon instance will be used in a production
        environment and the inline instance for testing or via the
        Python interpreter.

        .. note::

            :mod:`unittest` barfs if the method under test exits :-(

        The distinction between daemon or inline is made during object
        initialisation.  If you specify a *pidfile* then it will assume
        you want to run as a daemon.

        """
        if self.pidfile is not None:
            super(Server, self).start()
        else:
            self._start_inline()

    @abstractmethod
    def stop(self):
        super(Server, self).stop()

    def _start_inline(self):
        """The inline variant of the :meth:`start` method.

        """
        log_msg = '%s server process' % type(self).__name__

        # Reset the internal event flag
        log.info('%s - starting ...' % log_msg)
        self.proc = multiprocessing.Process(target=self._start_server,
                                            args=(self.exit_event,))
        self.proc.start()
        log.info('%s - started with PID %d' % (log_msg, self.proc.pid))
        time.sleep(0.1)         # can do better -- check TODO.

        # Flag the server as being operational.
        if self.proc.is_alive():
            self.pid = self.proc.pid

    def run(self):
        self._start_server(self.exit_event)
