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

    Initialisation will attempt a connection to the FTP server.
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

        self._connect()

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

        download_status = True
        log_msg = ('%s - download of "%s" to "%s"' % (type(self).__name__,
                                                      remotename,
                                                      localname))

        try:
            temp_fs = tempfile.NamedTemporaryFile(dir=os.curdir)
            self.client.retrbinary('RETR %s' % remotename,
                                   open(temp_fs.name, 'wb').write)

            # Transfer was successful so flag temporary file as persistent
            # so that the NamedTemporaryFile does not throw exception when
            # it tries to delete.
            temp_fs.delete = False
            os.rename(temp_fs.name, localname)
            log.info('%s OK' % log_msg) 
        except (OSError, ftplib.error_perm) as err:
            download_status = False
            log.warn('%s failed: "%s"' % (log_msg, str(err))) 
        finally:
            return download_status

    def upload(self, localname, remotename=None):
        """Place a file onto the server resource.

        **Args:**
            localname (str): Name of the file to send to the server

        **Kwargs:**
            remotename (str): Name of sent file to use on the server.  If a
            name is not provided then the name of the sent file is
            used (default).

        """
        if remotename is None:
            remotename = localname

        upload_status = True
        log_msg = ('%s - upload of "%s" to "%s"' % (type(self).__name__,
                                                    localname,
                                                    remotename))

        try:
            self.client.storbinary(('STOR %s' % remotename),
                                   open(localname, 'rb'))
            log.info('%s OK' % log_msg) 
        #except ftplib.error_perm as err:
        except all as err:
            upload_status = False
            log.warn('%s failed: "%s"' % (log_msg, str(err))) 
        finally:
            return upload_status

    def _connect(self):
        """Initiate the connection to the FTP server.

        """
        self._debug('connecting "%s" ...' % self.addr)
        self.client.connect(host=self.host, port=self.port)
        self._debug('login "%s" ...' % self.addr)
        self.client.login(self.user)

    def quit(self):
        """Wrapper around the :class:`ftplib.FTP` class `quit` method.

        Initiates a polite way to close a connection.

        """
        self.client.quit()

    def _debug(self, log_msg):
        """Wrapper method around the debug logging level which adds a bit
        more verbose information.
        """
        name = "%s.%s" % (type(self).__module__, type(self).__name__)
        log.debug('%s - %s' % (name, log_msg))
