"""
@author: pjay
"""

import hashlib
import BaseHTTPServer

import os
import urlparse
import itt
from itt.utils.log import log, class_logging

class HttpRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """Provides a custom HTTP request handler for ITT purposes.
    """
    
    contentSent = ''

    RANDOM_PATH = '/testing/dev/random'
    NULL_PATH = '/testing/dev/null'

    DEFAULT_BYTES = 1024
    
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

        url = urlparse.urlparse(self.path)
        qs = urlparse.parse_qs(url.query)

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()

        ##  Check for "special" paths, otherwise try and read real files
        if url.path == self.RANDOM_PATH:

            ##  Setup test content
            bytes = self.DEFAULT_BYTES
            if 'bytes' not in qs:
                log.warning("Query string does not specify 'bytes', but random data requested")
                log.warning("Using %s bytes by default" % self.DEFAULT_BYTES)
            else:
                bytes = qs['bytes']

            content = itt.TestContent(None, bytes=bytes)

            ##  Setup test configuration
            config = itt.TestConfig()
            if 'minimum_gap' in qs:
                config.minimum_gap = qs['minimum_gap']
            if 'chunk_size' in qs:
                config.chunk_size = qs['chunk_size']

        else if url.path == self.NULL_PATH:
            pass
        else:
            pass

        ##  connection = None, as the client has created the connection
        test = itt.Test(config, content, None)

        log.info("HTTP GET request finished for %s on port %s for %s\n   Resulting SHA1 sum of content: %s" % (
           self.client_address[0],
           self.client_address[1],
           self.path,
           hashlib.sha1(self.contentSent).hexdigest(),
        ))
