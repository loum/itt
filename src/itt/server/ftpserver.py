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
    """Simple FTP server built on top of the :mod:`pyftpdlib` module's
    :class:`ftpserver` class.
    """

    def __init__(self,
                 root,
                 port=2121):
        """FtpServer initialiser.

        Creates a FTP server that listens on port `port` and serves/writes
        to directory root specified by `root`.

        **Args:**
            root (str): Directory local to the server that will serve/write
                        file.

        **Kwargs:**
            port (int): Port that the server process listens on
                        (default=2121)
        """
        super(FtpServer, self).__init__()
        self.root = root
        self.port = port
        self.exit = multiprocessing.Event()

        self._authorizer = ftpserver.DummyAuthorizer()
        self._authorizer.add_anonymous(self.root)

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
        """
        log_msg = 'FTP server process'

        # Reset the internal event flag
        log.info('%s - starting ...' % log_msg)
        self.proc = multiprocessing.Process(target=self._run_server,
                                                args=(self.exit,))
        self.proc.start()
        log.info('%s - started with PID %d' % (log_msg, self.proc.pid))
        time.sleep(0.01)         # can do better -- check TODO.

    def _run_server(self, event):
        """
        """
        signal.signal(signal.SIGINT, self.signal_handler)

        server = ftpserver.FTPServer(self._address, self._ftp_handler)
        while not event.is_set():
            server.serve_forever(timeout=0.1, count=1)

        event.clear()

        log_msg = 'FTP server process'
        log.info('%s - stopping server ...' % log_msg)
        server.close_all()

    def stop(self):
        """
        """
        log_msg = 'FTP server process'
        log.info('%s - setting terminate flag ...' % log_msg)
        self.exit.set()

    def signal_handler(self, signal, frame):
        log.info('Ctrl-C intercepted ...')
        self.stop()
