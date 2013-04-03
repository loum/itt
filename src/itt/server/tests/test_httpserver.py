import unittest2
import multiprocessing
import time

import itt

def setUpModule():
    global _proc
    _proc = None

class TestHttpServer(unittest2.TestCase):

    def test_init(self):
        """Do nothing for now.
        """
        return

    def test_server_start(self):
        """Test HTTP server starts without errors.
        """
        global _proc

        server = itt.HttpServer()

        _proc = multiprocessing.Process(target=server.start)
        _proc.daemon = True
        _proc.start()

        print('Started HTTP server')
        time.sleep(0.25)

    def test_server_stop(self):
        """Test HTTP server stops without errors.
        """
        global _proc
        print _proc
        _proc.terminate()

        print('Stopped HTTP server')
