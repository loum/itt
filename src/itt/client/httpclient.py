#!/usr/bin/env python

'''
@author: pjay
'''

import optparse
import requests
import hashlib
import time
import sys
import httplib
import socket
import urlparse
import os

import itt
from itt.utils.log import log, class_logging

class HttpClient(itt.Client):
    '''Provides a HTTP client for uploads & downloads
    '''

    def getGap(self):
        ##  Do we have minimum packet gaps?
        min_gap = float(0.0)
        if self.test.config.minimum_gap is not None:
            min_gap = float(self.test.config.minimum_gap)
            log.info("  minimum_gap     : %s seconds" % min_gap)
        return min_gap

    def getChunk(self):
        ##  Do we have maximum chunk sizes?
        chunk = int(0)
        if self.test.config.chunk_size is not None:
            chunk = int(self.test.config.chunk_size)
            log.info("  chunk_size      : %s bytes" % chunk)
        return chunk

    def download(self):
        
        try:
            log.info("HTTP client begins download (HTTP GET):")

            bytes_qs = ""

            if self.test.content.static:
                url_path = self.test.content.filename
                log.info("  content: %s" % url_path)
            else:
                url_path = "/testing/dev/random"
                log.info("  content         : (random data)")
                log.info("  size            : %s bytes" % self.test.content.bytes)
                bytes_qs = "&bytes=%s" % (
                    self.test.content.bytes,
                )

            min_gap = self.getGap()
            chunk = self.getChunk()

            generated_url = urlparse.urljoin(
                "http://%s" % self.test.connection.netloc,
                "%s?minimum_gap=%s&chunk_size=%s%s" % (
                    url_path,
                    min_gap,
                    chunk,
                    bytes_qs,  ##  May be set to "&bytes=x" if random data
                ),
            )
            log.info("  url             : %s" % generated_url)

            download = requests.get(generated_url)
            shasum = hashlib.sha1(download.content).hexdigest()
            log.info("HTTP client finishes download (HTTP GET):")
            log.info("  url             : %s" % generated_url) 
            log.info("  received        : %s bytes" % len(download.content))
            log.info("  sha1_sum        : %s" % shasum)
            log.info("  http_response   : %s" % (download.status_code))
        except requests.ConnectionError, e:
            log.error("Download (HTTP GET) failed with a connection error: %s" % (str(e)))

    def upload(self):
        HTTP_DEVNULL = "/testing/dev/null"

        ##  Size of data
        bytes = int(0)

        try:
            log.info("HTTP client begins upload (HTTP POST):")
            generated_url = "http://%s/%s" % (
                self.test.connection.netloc,
                HTTP_DEVNULL,
            )
            log.info("  url             : %s" % generated_url)

            if self.test.content.static:
                log.info("  content         : %s" % self.test.content.filename)
            else:
                log.info("  content         : (random data)")

            bytes = self.test.content.bytes
            log.info("  size            : %s bytes" % bytes)

            min_gap = self.getGap()
            chunk = self.getChunk()

            ##  Open the file for sending
            self.test.content.open()
            ##  Open HTTP connection & send headers
            http = self.setupUploadConnection(HTTP_DEVNULL)

            ##  Send data
            i = int(0)
            while i < bytes:
                if chunk > 0:
                    ##  Send only as much as we're allowed
                    data = self.test.content.read(bytes=chunk)
                    if data == "":
                        ##  File was shorter than we thought?
                        break
                    
                    self.addAndSend(http, data)

                    i = i + chunk
                    
                    ##  Sleep for the minimum gap size
                    if i < bytes:
                        time.sleep(min_gap)

                else:
                    ##  Send everything as fast as possible
                    self.addAndSend(http, self.test.content.read())

                    i = i + bytes

            ##  Close the file
            self.test.content.close()

            ##  XXX: todo: generalise the sha1sum stuff
            shasum = hashlib.sha1(self.sent_data).hexdigest()
            log.info("HTTP client finishes upload (HTTP POST):")
            log.info("  url             : %s" % generated_url)
            log.info("  sent            : %s bytes" % len(self.sent_data))
            log.info("  sha1_sum        : %s" % shasum)

            ##  XXX: todo: if response ==200, else: error
            response = http.getresponse()
            log.info("  http_response   : %s" % (
                response.status,
            ))

        except (socket.error, httplib.HTTPException), e:
            log.error("Upload (HTTP POST) failed with an error: %s" % (str(e)))
            return

    def setupUploadConnection(self, path):
        HTTP_TIMEOUT = 20
        
        http = httplib.HTTPConnection(self.test.connection.netloc, timeout=HTTP_TIMEOUT)     ##  Un-hardcode timeout?

        http.putrequest("POST", path)
        http.putheader("content-type", "application/octet-stream")

        http.putheader("content-length", self.test.content.bytes)

        http.endheaders()

        return http

    def addAndSend(self, http, data):
        if not hasattr(self, 'sent_data'):
            self.sent_data = ""
        
        http.send(data)
        self.sent_data = "%s%s" % (
            self.sent_data,
            data,
        )
