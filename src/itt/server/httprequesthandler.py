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

        ##  Deal with (potential) query strings
        if self.path.find('?') != -1:
            path, qs = self.path.split('?')
        else:
            path = self.path
            qs = ''
        qs = urlparse.parse_qs(qs)

        min_gap = float(0.0)
        chunk = int(0)
        ##  Setup test configuration
        config = itt.TestConfig()
        if 'minimum_gap' in qs:
            min_gap = float(qs['minimum_gap'][0])
            config.minimum_gap = min_gap
        if 'chunk_size' in qs:
            chunk = int(qs['chunk_size'][0])
            config.chunk_size = chunk

        ##  Set bytes to something, overwrite in if-block below
        bytes = self.DEFAULT_BYTES

        ##  Check for "special" paths, otherwise try and read real files

        if path == self.RANDOM_PATH:
        ##  Send random data
            if 'bytes' not in qs:
                log.warning("Query string does not specify 'bytes', but random data requested")
                log.warning("Using %s bytes by default" % self.DEFAULT_BYTES)
            else:
                bytes = int(qs['bytes'][0])
            content = itt.TestContent(None, bytes=bytes)

        elif path == self.NULL_PATH:
        ##  Send nothing
            bytes = 0
            content = itt.TestContent(None, bytes=bytes)

        else:
        ##  Send real files from the servers' root
            content = itt.TestContent(path)

        ##  connection = None, as the client has created the connection
        self.test = itt.Test(config, content, None)

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
                if i < bytes:
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
