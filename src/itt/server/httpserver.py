#!/usr/bin/env python

"""
@author: pjay
"""

##  Hack for running HttpServer from itself; ie. python httpserver.py
import sys
sys.path.insert(0, "../..")

import BaseHTTPServer
import signal

import itt
from itt.utils.log import log, class_logging


@class_logging
class HttpServer(itt.Server):
    """Provides a HTTP server which is built on top of the
    :mod:`BaseHTTPServer` module.

    Example usage of the default settings as follows ...

    >>> import itt
    >>> server = itt.HttpServer(root='/tmp',
    ...                         request_handler=itt.HttpRequestHandler)
    >>> server.start()
    ...

    To terminate;

    >>> server.stop()

    """
    def __init__(self,
                 root,
                 bind='localhost',
                 port=8000,
                 pidfile=None,
                 request_handler=None):
        """HttpServer initialiser.

        Creates a HTTP server that listens on port *port* and server/writes
        to directory *root*.

        Specify a writable *pidfile* location to invoke the HTTP service
        as a daemon.

        .. warning::

            Don't try to run as a daemon with the :mod:`unittest` module.

        **Args:**
            root (str): Directory local to the server that will serve/write
            file.

        **Kwargs:**
            bind (str): The host address that will form part (host, port)
            for the socket to bind to as its source address before
            connecting.
            *bind* value 0.0.0.0 implies any address in a Linux environment.
            (default='localhost')

            port (int): Port that the server process listens on
            (default=2121)

            pidfile (string): Name of the PID file.  Only required if
            intending to run the module as a daemon.

            request_handler: HTTP request handler object.

        """
        super(itt.HttpServer, self).__init__(pidfile=pidfile)

        self.root = root
        self.bind = bind
        self.port = int(port)
        self.handler = request_handler

    def _start_server(self, event):
        """Instantiates a HTTP server.

        .. note::

            Some black magic here to overcome the :method:`SocketServer.serve_forever`
            from blocking program flow ...

            The :method:`_exit_handler` is given the object itself as an argument.  This
            creates a closure so that :method:`_exit_handler` can access the server object's
            :method:`SocketServer.shutdown` method.

        """
        self.server = BaseHTTPServer.HTTPServer((self.bind, self.port),
                                                self.handler)

        ##  Python crazyness: setting a variable inside the server object
        ##  that was never coded for by the Python standard lib programmers
        self.server.root = self.root

        print "XXX:1"
        # Prepare the environment to handle SIGTERM.
        #signal.signal(signal.SIGTERM, self._exit_handler(self.server))
        ## XXX: this is causing problems

        print "XXX:2"
        # Call the SocketServer.py module serve_forever method.
        log_msg = '%s --' % type(self).__name__
        print "XXX:3"
        log.debug('%s preparing server to handle requests ...' % log_msg)
        self.server.serve_forever()

    def _exit_handler(self, server_obj):
        log_msg = '%s --' % type(self).__name__
        log.info('%s SIGTERM intercepted' % log_msg)
        server_obj.shutdown()
        log.debug('%s terminated' % log_msg)

if __name__ == '__main__':
    myServer = itt.HttpServer('/tmp',
        bind='',
        request_handler=itt.HttpRequestHandler,
    )
    try:
        print "HTTP server starting"
        print "CTRL+C to terminate"
        myServer.start()
        while 1:
            ##  We're serving HTTP
            pass
    except KeyboardInterrupt:
        pass
    print "\nHTTP server terminating"
    myServer.stop()
