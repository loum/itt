import unittest2
import itt

#from utils.files import dummy_filesystem

class TestFtpServer(unittest2.TestCase):

    def test_init(self):
        """Do nothing for now.
        """
        return

    def test_server_start(self):
        """Test FTP server starts without errors.
        """
        server = itt.FtpServer()

        server.start()

        print('inside test_server_start()')
