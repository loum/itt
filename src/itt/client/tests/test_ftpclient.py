import unittest2

import itt
#from utils.files import dummy_filesystem

class TestFtpClient(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        # Start the FTP server.
        cls._server = itt.FtpServer(root='/tmp')
        cls._server.start()

    def test_init_no_args(self):
        """Test construction of the IP Test Tool FtpClient class.
        """
        self.assertRaises(TypeError, itt.FtpClient)

    def test_ftp_server(self):
        """Test FTP file downloads and uploads.
        """
        # Set up the client.
        client = itt.FtpClient(host='localhost', port=2121)
        client.download('banana')

    @classmethod
    def tearDownClass(cls):
        cls._server.stop()
