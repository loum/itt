import unittest2

import itt


class TestHttpServer(unittest2.TestCase):

    def test_init(self):
        """Test initialisation of the HttpServer.
        """
        with self.assertRaises(TypeError):
            itt.HttpServer()

        # Default port.
        http = itt.HttpServer(root='/tmp')
        expected = 8000
        received = http.port
        msg = ('Default HTTP server port should be: %s - received %s' %
                (str(expected), str(received)))
        self.assertEqual(received, expected, msg)
        http = None

        # Overridden port.
        received = port_to_use = 80011
        http = itt.HttpServer(root='/tmp', port=port_to_use)
        expected = http.port
        msg = ('Overridden HTTP server port should be: %s - received %s' %
               (str(expected), str(received)))
        self.assertEqual(received, expected, msg)
        http = None

    def test_server_start(self):
        """Test HTTP server starts without errors.
        """
        server = itt.HttpServer(root='/tmp',
                                request_handler=itt.HttpRequestHandler)
        msg = 'Inline HTTP server start should return True'
        self.assertTrue(server.start(), msg)

        # We should have a valid PID.
        msg = 'HTTP server process should have a valid PID'
        self.assertNotEqual(None, server.pid, msg)

        import time
        time.sleep(0.5)

        # Check that the server was shutdown.
        msg = 'HTTP server process stop should return True'
        self.assertTrue(server.stop(), msg)
        msg = 'HTTP server PID should be None'
        self.assertEqual(None, server.pid, msg)
