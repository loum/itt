import unittest2
import time
import os.path

import itt.utils
from itt.utils.files import dummy_filesystem


class DummyDaemon(itt.utils.Daemon):
    def _start_server(self, event):
        while True:
            time.sleep(1)


class TestDaemon(unittest2.TestCase):

    def setUp(self):
        # Create a location for our PID.
        self._temp_fs = dummy_filesystem()
        self._pid_file = self._temp_fs.name
        self._temp_fs.close()

    def test_init_of_abstract_class(self):
        """Test initialisation of the abstract Daemon class.
        """
        with self.assertRaises(TypeError):
            itt.utils.Daemon(self._pid_file)

    def test_init_with_no_arguments(self):
        """Test initialisation with no arguments.
        """
        with self.assertRaises(TypeError):
            DummyDaemon()

    def test_init_with_pidfile_none(self):
        """Test exception generation if no PID file is specified.
        """
        daemon = DummyDaemon(pidfile=None)
        with self.assertRaises(itt.utils.DaemonError):
            daemon._start_daemon()

    def test_init_with_unwritable_pid_file(self):
        """Test initialisation with unwritable PID file.
        """
        # But won't work if run as root :-(.
        unwritable_pid_file = '/pid'
        with self.assertRaises(IOError):
            DummyDaemon(pidfile=unwritable_pid_file)

    def test_start_with_existing_pid_file(self):
        """Test start with existing PID file.
        """
        # Open local instance of a PID file to simulate existing file.
        temp_fs = dummy_filesystem()
        pid_file = temp_fs.name

        # Set up the daemon.
        daemon = DummyDaemon(pidfile=pid_file)
        msg = 'Daemon start status existing PID file should be False'
        self.assertFalse(daemon.start(), msg)

        # Clean up.  
        temp_fs.close()

    def test_init_with_valid_pid_file(self):
        """Test initialisation of the Daemon with valid PID file.
        """
        daemon = DummyDaemon(pidfile=self._pid_file,
                             term_parent=False)
        msg = 'PID file error -- expected "%s", received "%s"'
        expected = self._pid_file
        received = daemon.pidfile
        self.assertEqual(expected, received, msg % (expected, received))

        # In this case, the PID file is empty which suggests that state
        # of process is idle.
        msg = 'Initial PID should be "None"'
        received = daemon.pid
        expected = None
        self.assertEqual(received, expected, msg)

        # File handle should be open for writing.
        msg = 'Initial PID file handle should be open for writing to.'
        received = daemon.pidfs.mode
        expected = 'w'
        self.assertEqual(received, expected, msg)

        # TODO: It would be really nice to test the start of the daemon.

    def test_stop_when_pid_file_exits_with_non_integer_value(self):
        """Test stop around PID file with non-integer value.
        """
        # Open local instance of a PID file to simulate empty file.
        temp_fs = dummy_filesystem()
        pid_file = temp_fs.name

        # Set up the daemon.
        daemon = DummyDaemon(pidfile=pid_file)
        msg = 'Daemon stop status for dodgy PID file should be False'
        self.assertFalse(daemon.stop(), msg)

        # Clean up.  
        temp_fs.close()

    def test_stop_with_pid_file_missing(self):
        """Test stop around missing PID file.
        """
        daemon = DummyDaemon(pidfile=self._pid_file)
        msg = 'Daemon stop status for missing PID file should be False'
        self.assertFalse(daemon.stop(), msg)

        msg = 'PID file should be removed if stop attempt on non-process'
        self.assertFalse(os.path.exists(self._pid_file), msg)

    def test_stop_non_existent_pid(self):
        """Test stop of an non-existent PID file.
        """
        # Open local instance of a PID file to simulate empty file.
        # This file will be deleted by the sttop() method make it persist
        # on the filesystem so that temporary file doesn't barf.
        temp_fs = dummy_filesystem(content='999999')
        temp_fs.delete = False
        pid_file = temp_fs.name

        # Set up the daemon.
        daemon = DummyDaemon(pidfile=pid_file)
        msg = 'Daemon stop status dodgy PID should be False'
        self.assertFalse(daemon.stop(), msg)

        # Check that the PID file was removed.
        msg = 'PID file "%s" was not removedi after dodgy PID' % pid_file
        self.assertFalse(os.path.exists(pid_file), msg)

    def tearDown(self):
        self._pid_file = None
        self._temp_fs = None
