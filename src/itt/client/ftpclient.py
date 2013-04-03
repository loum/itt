__all__ = [
    "FtpClient",
]

import ftplib

import itt
from itt.utils.log import log, class_logging


@class_logging
class FtpClient(itt.Client):
    """IP Test Tool FTP client class.

    """
    def __init__(self,
                 host,
                 port=2121,
                 user='anonymous'):
        """FtpClient class initialisation.

        """
        super(FtpClient, self).__init__()
        self.host = host
        self.port = port
        self.client = ftplib.FTP()
        self._user = 'anonymous'

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        self._user = value

    def download(self, remotename, localname=None):
        """
        """
        log_msg = 'FTP client'
        log.debug('%s - connecting to host "%s:%d" ...' % (log_msg,
                                                           self.host,
                                                           self.port))
        self.client.connect(host=self.host,
                            port=self.port)
        log.debug('%s - login to host "%s:%d" ...' % (log_msg,
                                                      self.host,
                                                      self.port))
        self.client.login(self.user)

    def upload(self, localname, remotename=None):
        """
        """
        return
