import unittest2
import tempfile
import os.path

import itt
from utils.files import dummy_filesystem

class TestFtpClient(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up the FTP server filesystem with some content.
        cls._test_content = 'FTP stuff'
        cls._temp_fs = dummy_filesystem(content=cls._test_content)

        # Given our dummy filesystem, make note of the directory and file
        # that will be presented by the FTP server.
        cls._test_dir = os.path.dirname(cls._temp_fs.name)
        cls._test_filename = os.path.basename(cls._temp_fs.name)

        print('test file name: %s' % cls._test_filename)

        # Start the FTP server.
        cls._server = itt.FtpServer(root=cls._test_dir)
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

        # Attempt to download a dodgy file.
        # Create a dummy target file.  We only want the name at this
        # point so let tempfile.NamedTemporaryFile clean up for us.
        temp_fs = tempfile.NamedTemporaryFile()
        dodgy_remote_file = os.path.basename(temp_fs.name)
        temp_fs.close()
        msg = 'Download of missing file should return False'
        self.assertFalse(client.download(dodgy_remote_file), msg)

        # Attempt a file download
        local_test_file = self._test_filename
        msg = 'Download of valid file should return True'
        self.assertTrue(client.download(self._test_filename), msg)

        # Check content.
        with open(local_test_file) as f:
            content = f.read()

        msg = 'FTP localfile post download has wrong content'
        received = content
        expected = self._test_content
        self.assertEqual(received, expected, msg)

        # TODO: file send

        # Cleanup.
        try:
            for file in [local_test_file]:
                os.remove(file)
        except:
            pass

    @classmethod
    def tearDownClass(cls):
        cls._test_content = None
        cls._temp_fs = None
        cls._test_dir = None
        cls._test_filename = None
        cls._server.stop()
