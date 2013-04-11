__all__ = [
    "TftpServer",
]

import multiprocessing
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

        self.port = port
        self.root = root
        self._server = None

    def __enter__(self):
        self.start()

        return self

    def __exit__(self, type, value, traceback):
        self.stop()
        self.server = None

    @property
    def server(self):
        return self._server

    @server.setter
    def server(self, value):
        self._server = value

    def start(self):
        """Wrapper around the server start process.  In ways, the start()
        method simulates the class context manager's __enter__ method.

        .. note::

            TODO - get rid of sleep around the port bind process  -- yuk

        **Returns**:
            (bool): value representing process' active state.

        """
        log_msg = 'TFTP server process'
        log.info('%s - starting ...' % log_msg)
        log.info('%s - serving root "%s" on port:%d' % (log_msg,
                                                        self.root,
                                                        self.port))
        self.proc = multiprocessing.Process(target=self._start_server)
        self.proc.start()
        time.sleep(0.2)         # can do better -- check TODO.

        # Flag the server as being operational.
        if self.proc.is_alive():
            self.pid = self.proc.pid

    def _start_server(self):
        """Responsible for the actual TFTP server start.

        Invokes the :meth:`tftpy.listen` method which starts the TFTP
        server's loop sequence for active connections.

        .. warning::

            Should not be called directly.  You probably want to call the
            :meth:`TftpServer.start` method instead.

        """
        self.server = tftpy.TftpServer(self.root)
        try:
            self.server.listen(listenport=self.port)
        except tftpy.TftpException as err:
            log.critical('%s' % str(err))

    def stop(self):
        """Responsible for the actual TFTP server stop (albeit in an
        un-graceful manner).

        Really only makes sense when used in daemon context as it will
        call the :class:`multiprocessing.Process` `terminate` method.

        .. note::

            If the TFTP server is used in serial context on the command
            line, Ctrl-C will do the trick.

        .. note::

            TODO - It would be really nice if shutdown could be managed
            gracefully ...

        """
        log_msg = 'TFTP server process'
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

    def run(self): pass
