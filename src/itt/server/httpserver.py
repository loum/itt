#!/usr/bin/env python

"""
@author: pjay
"""

##  Hack for running HttpServer from itself; ie. python httpserver.py
import sys
sys.path.insert(0, "../..")

##  Normal imports
import BaseHTTPServer
from signal import SIGTERM

import itt
from itt.utils.log import log, class_logging


class HttpServer(itt.Server):
    """Provides a HTTP server.
    """

    def __init__(self,
                 bind='localhost',
                 port=8000,
                 request_handler=None):
        """HttpServer initialiser.
        """
        super(HttpServer, self).__init__()

        self.port = port
        self.bind = bind
        self.server = None
        self.handler = request_handler

    def sigterm_handler(self, signum, frame):
        """Handle being killed.
        """
        log_msg = 'HTTP server process'
        log.info('%s - terminate signalled ...' % log_msg)

        self.stop()

    def start(self):
        """Wrapper around the server start process.
        """
        log_msg = 'HTTP server process'
        log.info('%s - starting ...' % log_msg)

        self._start_server()

    def _start_server(self):
        """Instantiates a HTTP server.
        """
        self.server = BaseHTTPServer.HTTPServer((self.bind, self.port), self.handler)
        self.server.serve_forever()

    def stop(self):
        """Kills a HTTP server.
        """
        log_msg = 'HTTP server process'
        log.info('%s - terminating ...' % log_msg)
        self.server.server_close()

    def run(self): pass

if __name__ == '__main__':
    myServer = itt.HttpServer(
        bind='',
        request_handler=itt.HttpRequestHandler,
    )
    try:
        print "HTTP server starting"
        print "CTRL+C to terminate"
        myServer.start()
    except KeyboardInterrupt:
        pass
    print "\nHTTP server terminating"
    myServer.stop()
