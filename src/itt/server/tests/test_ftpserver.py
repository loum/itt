import unittest2
import socket
import os
import signal
import time

import itt


class TestFtpServer(unittest2.TestCase):

    def test_init(self):
        """Test initialisation of the FtpServer.
        """
        with self.assertRaises(TypeError):
            itt.FtpServer()

        # Default port.
        ftp = itt.FtpServer(root='/tmp')
        expected = 2121
        received = ftp.port
        msg = ('Default FTP server port should be 2121 - received %s' %
               str(received))
        self.assertEqual(received, expected, msg)
        ftp = None

        # Overriden port.
        received = port_to_use = 2122
        tftp = itt.FtpServer(root='/tmp', port=port_to_use)
        expected = tftp.port
        msg = ('Overriden port value should be 2122 - received %s' %
               str(received))
        self.assertEqual(received, expected, msg)
        ftp = None

    def test_server_daemon(self):
        """Test FTP server daemon start and stop.
        """
        server = itt.FtpServer(root='/tmp')
        server.start()
        self.port_checker('127.0.0.1', server.port)

        # We should have a valid PID.
        msg = 'FTP server process should have a valid PID'
        self.assertNotEqual(None, server.pid, msg)

        # Now stop the daemon.
        server.stop()

        # Allow time until server releases resources - ugly.
        time.sleep(0.1)

        # PID should be unset.
        msg = 'FTP server PID should not be None'
        self.assertEqual(None, server.pid, msg)

        # Will throw exception if previous process is still bound.
        server.start()
        self.port_checker('', server.port)
        pid = server.proc.pid
        os.kill(pid, signal.SIGTERM)

    def port_checker(self, host, port):
        with self.assertRaises(socket.error) as cm:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((host, port))

        # Verify that exception code.
        (errno, err_msg) = cm.exception
        expected = 98           # Code 98 for 'Address already in use'
        received = errno
        msg = ('Port bind should generate error code 98 - received %d' %
               received)
        self.assertEqual(expected, received, msg)
