import unittest2
import os.path

import itt
from itt.utils.files import dummy_filesystem


class TestTftpServer(unittest2.TestCase):

    def test_init(self):
        """Test initialisation of the TftpServer.
        """
        with self.assertRaises(TypeError):
            itt.TftpServer()

    def setUp(self):
        self.test_content = 'temp TFTP stuff'
        self.temp_fs = dummy_filesystem(content=self.test_content)
        self.test_dir = os.path.dirname(self.temp_fs.name)

        # Default port.
        tftp = itt.TftpServer(root='/tmp')
        expected = 6969
        received = tftp.port
        msg = ('Default TFTP port should be 6969 - received %s' %
               str(received))
        self.assertEqual(received, expected, msg)
        tftp = None

        # Overriden port.
        received = port_to_use = 6970
        tftp = itt.TftpServer(root='/tmp', port=port_to_use)
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
        msg = 'TFTP server process should have a valid PID'
        self.assertNotEqual(None, server.pid, msg)

        # Check that the server was shutdown.
        server.stop()
        msg = 'TFTP server PID should not None'
        self.assertEqual(None, server.pid, msg)

    def tearDown(self):
        self.test_content = None
        self.temp_fs = None
        self.temp_dir = None

if __name__ == '__main__':
    unittest2.main()
