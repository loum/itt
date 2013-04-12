__all__ = [
    "FtpServer",
]

from pyftpdlib import ftpserver
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

    .. note::

        Refer to :class:`itt.server.Server` for the attributes list.

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

        self._authorizer = ftpserver.DummyAuthorizer()
        self._authorizer.add_anonymous(self.root, perm='elrw')

        self._ftp_handler = ftpserver.FTPHandler
        self._ftp_handler.authorizer = self._authorizer

        self._address = ('127.0.0.1', self.port)

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

        self.server = ftpserver.FTPServer(self._address, self._ftp_handler)
        while not event.is_set():
            self.server.serve_forever(timeout=0.1, count=1)

        event.clear()

        log.info('%s - stopping server ...' % type(self).__name__)
        self.server.close_all()

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
        log.info('%s - setting terminate flag ...' % type(self).__name__)
        self.exit_event.set()

        # Flag the server as not operational.
        self.pid = None

    def _signal_handler(self, signal, frame):
        log.info('%s SIGTERM intercepted' % type(self).__name__)
        self._set_exit_handler()
