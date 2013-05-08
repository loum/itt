import unittest2
import tempfile
import os.path
import time

import itt
from itt.utils.files import dummy_filesystem

class TestTftpClient(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up the TFTP server filesystem with some content.
        cls._test_content = 'TFTP stuff'
        cls._temp_fs = dummy_filesystem(content=cls._test_content)

        # Given our dummy filesystem, make note of the directory and file
        # that will be presented by the TFTP server.
        cls._test_dir = os.path.dirname(cls._temp_fs.name)
        cls._test_filename = os.path.basename(cls._temp_fs.name)

        # Start the TFTP server.
        cls._server = itt.TftpServer(root=cls._test_dir)
        cls._server.start()

    def test_init_no_args(self):
        """Test constructon of the IP Test Tool TftpClient class.
        """
        self.assertRaises(TypeError, itt.TftpClient)

    def test_tftp_server(self):
        """Test TFTP file downloads and uploads.
        """
        # Set up the client.
        client = itt.TftpClient(host='localhost', port=6969)

        # Attempt a file retrieve.
        client.download(self._test_filename)

        # If successful, the retrieved file should appear in the current
        # directory.
        local_test_file = self._test_filename
        msg = 'Retrieved file "%s" does not exist locally' % local_test_file
        self.assertTrue(os.path.exists(local_test_file), msg)
        
        # Check content.
        content = None
        with open(local_test_file) as f:
            content = f.read()

        msg = 'TFTP localfile post download has wrong content'
        received = content
        expected = self._test_content
        self.assertEqual(received, expected, msg)

        # Now attempt a file send.
        # Create a dummy target file.  We only want the name at this
        # point so let tempfile.NamedTemporaryFile clean up for us.
        temp_fs = tempfile.NamedTemporaryFile()
        remote_file = os.path.basename(temp_fs.name)
        temp_fs.close()

        # Just reuse the file that we previously downloaded.
        client.upload(local_test_file, remote_file)

        # Give the transfer some time to end -- (yuk!!!)
        time.sleep(1)

        # Check if the target file hit the server root.
        target_file = os.path.join(self._test_dir, remote_file)
        msg = 'Sent file "%s" does not exist in server root' % target_file
        self.assertTrue(os.path.exists(target_file), msg)

        # Check the contents of the sent file.
        content = None
        with open(target_file) as fh:
            content = fh.read()

        msg = 'TFTP sent file has wrong content'
        received = content
        expected = self._test_content
        self.assertEqual(received, expected, msg)

        # Cleanup.
        try:
            for file in [local_test_file, target_file]:
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
