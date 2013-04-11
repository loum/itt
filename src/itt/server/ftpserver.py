__all__ = [
    "FtpServer",
]

import multiprocessing
from pyftpdlib import ftpserver
import time
import signal

import itt
from itt.utils.log import log, class_logging


@class_logging
class FtpServer(itt.Server):
    """Simple FTP server built on top of the :class:`pyftpdlib.ftpserver`
    class.

    Example usage of the default settings as follows using the directory
    ``/tmp`` as the FTP server's root:

    >>> from itt.server.ftpserver import FtpServer
    >>> server = FtpServer(root='/tmp')
    >>> server.start()
    ...

    By default, this will bind the FTP server to 127.0.0.1:2121

    From here, use your preferred FTP client to interface with the server.

    To stop the FTP server:

    >>> server.stop()

    Alternatively, "kill -s SIGTERM <pid>" will also do the trick.

    """
    def __init__(self,
                 root,
                 port=2121,
                 pidfile=None):
        """FtpServer initialiser.

        Creates a FTP server that listens on port `port` and serves/writes
        to directory root specified by `root`.

        Specify a writable *pidfile* location to invoke the FTP service
        as a daemon.

        .. warning::

            Don't try to run as a daemon with the :mod:`unittest` module.

        **Args:**
            root (str): Directory local to the server that will serve/write
            file.

        **Kwargs:**
            port (int): Port that the server process listens on
            (default=2121)

            pidfile (string): Name of the PID file.  Only required if
            intending to run the module as a daemon.

        .. warning::

            TODO -- currently, the anonymous user has write permissions to
            the the directory.  We probably want to create a valid user
            and tailor permissions around required usage.

        """
        super(itt.FtpServer, self).__init__(pidfile=pidfile)

        self.root = root
        self.port = port
        self.exit = multiprocessing.Event()

        self._authorizer = ftpserver.DummyAuthorizer()
        self._authorizer.add_anonymous(self.root, perm='elrw')

        self._ftp_handler = ftpserver.FTPHandler
        self._ftp_handler.authorizer = self._authorizer

        self._address = ('127.0.0.1', self.port)

    @property
    def exit(self):
        return self._exit

    @exit.setter
    def exit(self, value):
        self._exit = value

    def start(self):
        """Wrapper around the FTP server start process.

        Invokes the FTP server one in two ways:

        * As a daemon
        * Inline using the :mod:`multiprocessing.Event` module

        Typically, the daemon instance will be used in a production
        environment and the inline instance for testing or via the
        Python interpreter.

        .. note::

            :mod:`unittest` barfs if the method under test exits :-(

        The distinction between daemon or inline is made during object
        initial.  If you specify a *pidfile* then it will assume you want
        to run as a daemon.

        """
        if self.pidfile is not None:
            super(itt.FtpServer, self).start()
        else:
            self._start_inline()

    def _start_inline(self):
        """The inline variant of the :meth:`start` method.

        """
        log_msg = 'FTP server process'

        # Reset the internal event flag
        log.info('%s - starting ...' % log_msg)
        self.proc = multiprocessing.Process(target=self._start_server,
                                            args=(self.exit,))
        self.proc.start()
        log.info('%s - started with PID %d' % (log_msg, self.proc.pid))
        time.sleep(0.01)         # can do better -- check TODO.

        # Flag the server as being operational.
        if self.proc.is_alive():
            self.pid = self.proc.pid

    def _start_server(self, event):
        """Responsible for the actual FTP server start.

        Invokes the :meth:`pyftpdlib.ftpserver.serve_forever` method and
        listens for incoming connections.

        .. warning::

            Should not be called directly.  You probably want to call the
            :meth:`FtpServer.start` method instead.

        **Args:**
            event (:mod:`multiprocessing.Event`): Internal semaphore that
            terminates the FTP server once it is set.

        """
        signal.signal(signal.SIGTERM, self._signal_handler)

        server = ftpserver.FTPServer(self._address, self._ftp_handler)
        while not event.is_set():
            server.serve_forever(timeout=0.1, count=1)

        event.clear()

        log_msg = 'FTP server process'
        log.info('%s - stopping server ...' % log_msg)
        server.close_all()

    def stop(self):
        """Wrapper around the FTP server stop process.
        """
        if self.pidfile is not None:
            super(itt.FtpServer, self).stop()
        else:
            self._set_exit_handler()

    def _set_exit_handler(self):
        """Responsible for the actual FTP server stop.
        """
        log_msg = 'FTP server process'
        log.info('%s - setting terminate flag ...' % log_msg)
        self.exit.set()

        # Flag the server as not operational.
        self.pid = None

    def _signal_handler(self, signal, frame):
        log.info('Termination signal intercepted ...')
        self._set_exit_handler()

    def run(self):
        self._start_server(self.exit)
