import unittest2
import itt
import os.path

from utils.files import dummy_filesystem

class TestTftpServer(unittest2.TestCase):

    def setUp(self):
        self.test_content = 'temp TFTP stuff'
        self.temp_fs = dummy_filesystem(content=self.test_content)
        self.test_dir = os.path.dirname(self.temp_fs.name)

    def test_init(self):
        """Test initialisation of the TftpServer.
        """
        with self.assertRaises(TypeError):
            tftp = itt.TftpServer()

        tftp = itt.TftpServer(root='/tmp')
        received = 6969
        expected = tftp.port
        msg = ('Default port value should be 6969 - received %s' %
               str(received))
        self.assertEqual(received, expected, msg)
        tftp = None

        tftp = itt.TftpServer(root='/tmp', port=6970)
        received = 6970
        expected = tftp.port
        msg = ('Overriden port value should be 6970 - received %s' %
               str(received))
        self.assertEqual(received, expected, msg)
        tftp = None

    def test_server_start(self):
        """Test TFTP server starts without error.
        """
        server = itt.TftpServer(root=self.test_dir)

        # Check that the server was started.
        server.start()
        msg = 'Server process should be active'
        self.assertTrue(server.proc.is_alive(), msg)

        # Check that the server was shutdown.
        server_state = server.stop()
        msg = 'Server process should not be active'
        self.assertFalse(server_state, msg)

    def tearDown(self):
        self.test_content = None
        self.temp_fs = None
        self.temp_dir = None

if __name__ == '__main__':
    unittest2.main()
