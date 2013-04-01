__all__ = [
    "FtpServer",
]

import multiprocessing
from pyftpdlib import ftpserver

import itt
from itt.utils.log import log, class_logging


@class_logging
class FtpServer(itt.Server):
    """
    """

    def __init__(self,
                 port=2121,
                 daemon=True):
        """FtpServer initialiser.
        """
        super(FtpServer, self).__init__()
        self.port = port
        self.daemon = daemon
        self.server = None

        self._authorizer = ftpserver.DummyAuthorizer()
        self._authorizer.add_anonymous('/tmp')

        self._ftp_handler = ftpserver.FTPHandler
        self._ftp_handler.authorizer = self._authorizer

        self._address = ('127.0.0.1', 2121)


    def start(self):
        """Wrapper around the server start process.
        """
        log_msg = 'FTP server process'
        log.info('%s - starting ...' % log_msg)

        if self.daemon:
            self.proc = multiprocessing.Process(target=self._start_server)
            self.proc.daemon = True
            self.proc.start()
        else:
            self._start_server()

    def _start_server(self):
        """
        """
        self.server = ftpserver.FTPServer(self._address, self._ftp_handler)
        self.server.serve_forever(count=10)

    def stop(self):
        """
        """
        log_msg = 'FTP server process'
        log.info('%s - terminating ...' % log_msg)
        self.server.close()

        if self.proc is not None:
            self.proc.terminate()

