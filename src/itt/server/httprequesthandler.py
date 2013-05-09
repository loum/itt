"""
@author: pjay
"""

import BaseHTTPServer

import hashlib
import os
import time
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

        min_gap = float(0.0)
        chunk = int(0)
        ##  Setup test configuration
        config = itt.TestConfig()
        if 'minimum_gap' in qs:
            min_gap = qs['minimum_gap']
            config.minimum_gap = min_gap
        if 'chunk_size' in qs:
            chunk = qs['chunk_size']
            config.chunk_size = chunk

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

        elif url.path == self.NULL_PATH:
            pass
        else:
            pass

        ##  connection = None, as the client has created the connection
        test = itt.Test(config, content, None)

        ##  Open the file for sending
        self.test.content.open()

        ##  Send headers
        self.send_response(200)
        self.send_header("content-type", "text/plain")
        self.send_header("content-length", self.test.content.bytes)
        self.end_headers()

        ##  Send data
        i = int(0)
        while i < bytes:
            if chunk > 0:
                ##  Send only as much as we're allowed
                data = self.test.content.read(bytes=chunk)
                if data == "":
                    ##  File was shorter than we thought?
                    break

                self.storeAndWrite(data, self.wfile)

                i = i + chunk

                ##  Sleep for the minimum gap size
                time.sleep(min_gap)

            else:
                ##  Send everything as fast as possible
                self.storeAndWrite(self.test.content.read(), self.wfile)

                i = i + bytes

        ##  Close the file
        self.test.content.close()

        log.info("HTTP GET request finished for %s on port %s for %s\n   Resulting SHA1 sum of content: %s" % (
           self.client_address[0],
           self.client_address[1],
           self.path,
           hashlib.sha1(self.contentSent).hexdigest(),
        ))
