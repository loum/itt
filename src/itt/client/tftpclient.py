__all__ = [
    "TftpClient",
]

import tftpy

import itt
from itt.utils.log import log, class_logging


@class_logging
class TftpClient(itt.Client):
    """IP Test Tool TFTP client class.

    Through the `download` and `upload` methods, the TftpClient class allows
    interaction with TFTP server infrastructure.

    Example usage when connecting to a TFTP server as follows ...

    Say I have a target TFTP server at "banana.com.au:6969", and I want to
    get a file called "banana.txt":

    >>> from itt.client import TftpClient
    >>> client = TftpClient(host='banana.com.au', port=6969)
    >>> client.download('banana.txt')
    2013-03-26 09:10:09,556 (INFO): Downloading remote file "banana.txt" ...

    Similarly, to upload a file use the `upload` method:
    >>> client.upload('banana.txt', 'new_uploaded_filename')
    2013-03-26 12:35:05,039 (INFO): Uploading local file "banana.txt" ...

    This will place the local file "banana.txt" on the server resource
    under the name "new_uploaded_filename".

    """
    def __init__(self, host, port):
        """TftpClient class initialisation.

        Creates a client object based on the port number according to the
        following:

            * port 6969 - TFTP client

        **Args:**
            host (str): The name of the server to connect to.
            port (int): The port number on the server.

        """
        super(TftpClient, self).__init__()
        self.host = host
        self.port = port
        self.client = None

        if self._port == 6969:
            self.create_tftp_session()

    def download(self, remotename, localname=None):
        """Retrieve a file from the server resource.

        **Args:**
            remotename (str): Name of the file to retrieve on the server

        **Kwargs:**
            localname (str): Name of retrived file on the local filesystem.
            If a name is not provided then the name of the retrieved file
            is used (default).
        """
        if localname is None:
            localname = remotename

        log.info('Downloading remote file "%s" to local file "%s"'
                 % (remotename, localname))
        self.client.download(remotename, localname)

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

        log.info('Uploading local file "%s" to remote file "%s"'
                 % (localname, remotename))
        self.client.upload(remotename, localname)

    def create_tftp_session(self):
        """
        """
        log.info('Port %d specified: creating TFTP client session'
                 % self.port)
        self.client = tftpy.TftpClient(self.host, self.port)
