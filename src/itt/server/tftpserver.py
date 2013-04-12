__all__ = [
    "TftpServer",
]

import sys
import signal
import tftpy
import time

import itt
from itt.utils.log import log, class_logging


@class_logging
class TftpServer(itt.Server):
    """Simple TFTP server built on top of the :mod:`tftpy` module's
    :class:`tftpy.TftpServer` class.

    Example usage of the default settings as follows ...

    Say I have a directory '/tmp' that will act as my server's root:

    >>> from itt.server.tftpserver import TftpServer
    >>> server = TftpServer('/tmp')
    >>> server.start()
    ...

    To terminate:

    >>> server.stop()

    The server can also be used within a ``with`` construct:

    >>> from itt.server.tftpserver import TftpServer
    >>> with TftpServer as server:
    >>>    ...

    The context manager will handle the server start and stop for
    you.  Nice!!!
    """

    def __init__(self,
                 root,
                 port=6969,
                 pidfile=None):
        """TftpServer initialiser.

        Creates a TFTP server that listens on port `port` and serves/writes
        to directory root specified by `root`.

        .. warning::

            Don't try to run as a daemon with the :mod:`unittest` module.

        **Args:**
            root (str): Directory local to the server that will serve/write
            file.
            
        **Kwargs:**
            port (int): Port that the server process listens on
            (default=6969)

            pidfile (string): Name of the PID file.  Only required if
            intending to run the module as a daemon.

        """
        super(TftpServer, self).__init__(pidfile=pidfile)

        self.port = int(port)
        self.root = root

    def __enter__(self):
        self.start()

        return self

    def __exit__(self, type, value, traceback):
        self.stop()
        self.server = None

    def _start_server(self, event):
        """Responsible for the actual TFTP server start.

        Invokes the :meth:`tftpy.listen` method which starts the TFTP
        server's loop sequence for active connections.

        .. warning::

            Should not be called directly.  You probably want to call the
            :meth:`TftpServer.start` method instead.

        **Args:**
            event (:mod:`multiprocessing.Event`): Internal semaphore that
            terminates the FTP server once it is set.

        """
        signal.signal(signal.SIGTERM, self._signal_handler)

        self.server = tftpy.TftpServer(self.root)
        try:
            self.server.listen(listenport=self.port)
        except tftpy.TftpException as err:
            log.critical('%s' % str(err))

    def stop(self):
        """Responsible for the actual TFTP server stop (albeit in an
        un-graceful manner).

        .. note::

            If the TFTP server is used in serial context on the command
            line, Ctrl-C will do the trick.

            TODO - It would be really nice if shutdown could be managed
            gracefully ...

        """
        stop_status = False

        if self.pidfile is not None:
            super(itt.TftpServer, self).stop()
        else:
            stop_status = self._exit_inline()

        return stop_status

    def _exit_inline(self):
        """
        """
        log_msg = type(self).__name__
        if self.proc is not None:
            log.info('%s - terminating ...' % log_msg)
            self.proc.terminate()

            while self.proc.is_alive():
                log.info('%s - waiting to terminate ...' % log_msg)
                time.sleep(0.001)

            log.info('%s - terminated.' % log_msg)
        else:
            log.warn('%s - not active' % log_msg)

        # Flag the server as not operational.
        self.pid = None

        return self.proc.is_alive()

    def _signal_handler(self, signal, frame):
        log.info('%s SIGTERM intercepted' % type(self).__name__)
        sys.exit(0)
