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

from types import *

import itt
from itt.utils.log import log, class_logging

class HttpClient(itt.Client):
    '''Provides a HTTP client for uploads & downloads
    '''

    def getGap(self):
        ##  Do we have minimum packet gaps?
        min_gap = float(0.0)
        if self.config.minimum_gap is not None:
            min_gap = float(self.config.minimum_gap)
            log.info("  minimum_gap     : %s seconds" % min_gap)
        return min_gap

    def getChunk(self):
        ##  Do we have maximum chunk sizes?
        chunk = int(0)
        if self.config.chunk_size is not None:
            chunk = int(self.config.chunk_size)
            log.info("  chunk_size      : %s bytes" % chunk)
        return chunk

    def download(self):
        
        try:
            log.info("HTTP client begins download (HTTP GET):")

            if self.config.content is not None:
                url_path = self.config.content
                log.info("  content: %s" % self.config.content)
            else:
                url_path = "/itt/testing/dev/random"
                log.info("  content         : (random data)")

            min_gap = self.getGap()
            chunk = self.getChunk()

            generated_url = "http://%s/%s?minimum_gap=%s&chunk_size=%s" % (
                self.config.netloc,
                url_path,
                min_gap,
                chunk,
            )

            ##  Size for random data...
            if self.config.content is None:
                log.info("  size            : %s bytes" % self.config.bytes)
                generated_url = "%s&bytes=%s" % (
                    generated_url,
                    self.config.bytes,
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
        HTTP_DEVNULL = "/itt/testing/dev/null"

        ##  Are we sending random data?
        random = False

        ##  Size of data
        bytes = int(0)

        try:
            log.info("HTTP client begins upload (HTTP POST):")
            generated_url = "http://%s/%s" % (
                self.config.netloc,
                HTTP_DEVNULL,
            )
            log.info("  url             : %s" % generated_url)

            if self.config.content is not None:
                random = False
                log.info("  content         : %s" % self.config.content)
                ##  Open file
                file = open(self.config.content, "rb")
                ##  How big is it?
                bytes = int(os.path.getsize(self.config.content))
            else:
                random = True
                log.info("  content         : (random data)")
                bytes = int(self.config.bytes)

            log.info("  size            : %s bytes" % bytes)

            min_gap = self.getGap()
            chunk = self.getChunk()

            ##  Open HTTP connection & send headers
            http = self.setupUploadConnection(HTTP_DEVNULL)

            ##  Send data
            i = int(0)
            while i < bytes:
                if chunk > 0:
                    ##  Send only as much as we're allowed
                    if not random:
                        data = file.read(chunk)
                        if data == "":
                            ##  File was shorter than we thought?
                            break
                    else:
                        data = os.urandom(chunk)
                    
                    self.addAndSend(http, data)

                    i = i + chunk
                    
                    ##  Sleep for the minimum gap size
                    time.sleep(min_gap)

                else:
                    ##  Send everything as fast as possible
                    if not random:
                        self.addAndSend(http, file.read())
                    else:
                        self.addAndSend(http, os.urandom(bytes))

                    i = i + bytes

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
        
        http = httplib.HTTPConnection(self.config.netloc, timeout=HTTP_TIMEOUT)     ##  Un-hardcode timeout?

        http.putrequest("POST", path)
        http.putheader("content-type", "application/octet-stream")

        ##  A quick note why we don't provide content-length: because we
        ##  don't want to have to pre-calculate it.  We don't have to
        ##  worry about progress bars, so lets leave it.
        ##  See: http://tech.hickorywind.org/articles/2008/05/23/content-length-mostly-does-not-matter-the-reverse-bob-barker-rule
        ##  http.putheader("content-length", len(???))

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
