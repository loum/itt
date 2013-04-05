__all__ = [
    "FtpClient",
]

import ftplib
import tempfile
import os

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

    @property
    def addr(self):
        return "%s:%d" % (self.host, self.port)

    def download(self, remotename, localname=None):
        """The :meth:`download` method is a wrapper around the
        :class:`tftplib.FTP` class :meth:`connect`, :meth:`download` and
        methods.

        Will attempt to download `remotename` to the local filesystem.  If
        `localname` is `None` then `localname` will be the same as
        `remotename`.

        The initial download is written to a
        :class:`tempfile.NamedTemporaryFile` object so that failed
        transfers are automatically cleaned up locally.  Successful
        transfers produce an atomic rename to `localname`.

        **Args:**
            remotename (str): Name of the file to retrieve on the server

        **Kwargs:**
            localname (str): Name of retrived file on the local filesystem.
            If a name is not provided then the name of the retrieved file
            is used (default).

        **Returns:**
            boolean::

                True - successful transfer
                False - failed transfer

        """
        if localname is None:
            localname = remotename

        # Initiate the connection to the server.
        self._debug('connecting "%s" ...' % self.addr)
        self.client.connect(host=self.host, port=self.port)
        self._debug('login "%s" ...' % self.addr)
        self.client.login(self.user)

        # Attempt the download.
        status = True
        try:
            temp_fs = tempfile.NamedTemporaryFile(dir=os.curdir)
            self.client.retrbinary('RETR %s' % remotename,
                                   open(temp_fs.name, 'wb').write)

            # Now rename the file.
            # Since the transfer was successful, then flag it as persistent
            # so that the NamedTemporaryFile does not throw exception when
            # it tries to delete.
            temp_fs.delete = False
            os.rename(temp_fs.name, localname)
        except (OSError, ftplib.error_perm) as err:
            status = False
        finally:
            log_msg = 'download of "%s" to "%s"' % (remotename, localname)
            if status:
                log.info('%s OK' % log_msg) 
            else:
                log.warn('%s failed: "%s"' % (log_msg, str(err))) 

            return status

    def upload(self, localname, remotename=None):
        """
        """
        return

    def _debug(self, log_msg):
        """Wrapper method around the debug logging level which adds a bit
        more verbose information.
        """
        name = "%s.%s" % (type(self).__module__, type(self).__name__)
        log.debug('%s - %s' % (name, log_msg))
