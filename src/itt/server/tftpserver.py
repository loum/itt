__all__ = [
    "TftpServer",
]

import signal
import tftpy
import sys

import itt
from itt.utils.log import log, class_logging


@class_logging
class TftpServer(itt.Server):
    """Simple TFTP server built on top of the :mod:`tftpy` module's
    :class:`tftpy.TftpServer` class.

    Example usage of the default settings as follows ...

    Say I have a directory '/tmp' that will act as my server's root:

    >>> import itt
    >>> server = itt.TftpServer('/tmp')
    >>> server.start()
    ...

    To terminate:

    >>> server.stop()

    The server can also be used within a ``with`` construct:

    >>> from itt.server.tftpserver import TftpServer
    >>> with TftpServer as server:
    ...    # do stuff here

    The context manager will handle the server start and stop for
    you.  Nice!!!

    """
    def __init__(self,
                 root,
                 port=6969,
                 pidfile=None):
        """TftpServer initialiser.

        Creates a TFTP server that listens on port *port* and serves/writes
        to directory *root*.

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
            :meth:`itt.TftpServer.start` method instead.

        **Args:**
            event (:mod:`multiprocessing.Event`): Internal semaphore that
            terminates the FTP server once it is set.

        """
        self.server = tftpy.TftpServer(self.root)

        # Prepare the environment to handle SIGTERM.
        signal.signal(signal.SIGTERM, self._exit_handler)

        try:
            log_msg = '%s --' % type(self).__name__
            self.server.listen(listenport=self.port)
            log.debug('%s listening on port: %d' % (log_msg, self.port))
        except tftpy.TftpException as err:
            log.critical('%s' % str(err))

    def _exit_handler(self, signal, frame):
        log_msg = '%s --' % type(self).__name__
        log.info('%s SIGTERM intercepted' % log_msg)
        sys.exit(0)
