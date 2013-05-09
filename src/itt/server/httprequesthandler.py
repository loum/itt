"""
@author: pjay
"""

import hashlib
import BaseHTTPServer

import itt
from itt.utils.log import log, class_logging

class HttpRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """Provides a custom HTTP request handler for ITT purposes.
    """
    
    contentSent = ''
    
    def storeAndWrite(self, str, wfile):
        """Store the string in self.contentSent, and write it to wfile)"""
        self.contentSent = self.contentSent + str
        wfile.write(str)
    
    def do_POST(self):
        """Response to a POST request."""
        log.info("HTTP POST request received from %s on port %s for %s" % (
            self.client_address[0],
            self.client_address[1],
            self.path,
        ))

        self.send_response(200)
        self.end_headers()

        received = self.rfile.read()

        log.info(
            "HTTP POST request finished for %s on port %s for %s\n" \
            "    Size of received content: %s\n" \
            "    Resulting SHA1 sum of content: %s" % (
                self.client_address[0],
                self.client_address[1],
                self.path,
                len(received),
                hashlib.sha1(received).hexdigest(),
        ))

    def do_GET(self):
        """Respond to a GET request."""
        log.info("HTTP GET request received from %s on port %s for %s" % (
            self.client_address[0],
            self.client_address[1],
            self.path,
        ))

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()

        ##  XXX: Todo, new functionality here

        log.info("HTTP GET request finished for %s on port %s for %s\n   Resulting SHA1 sum of content: %s" % (
           self.client_address[0],
           self.client_address[1],
           self.path,
           hashlib.sha1(self.contentSent).hexdigest(),
        ))
