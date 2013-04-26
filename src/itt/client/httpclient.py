#!/usr/bin/env python

'''
@author: pjay
'''

##  Hack for running HttpClient from itself; ie. ./httpclient.py
import sys
sys.path.insert(0, "../..")

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

    def download(self):
        log.info("HTTP client begins download (HTTP GET): %s" % (self.opts.url))
        try:
            print urlparse.urlsplit(self.opts.url)
            download = requests.get(self.opts.url)
            log.info("HTTP client finishes download (HTTP GET): %s" % (self.opts.url))
            if download.status_code == 200:
                shasum = hashlib.sha1(download.content).hexdigest()
                log.info("SHA1 sum of content received: %s" % (shasum))
            else:
                log.error("Download (HTTP GET) failed with status code: %s" % (download.status_code))
        except requests.ConnectionError, e:
            log.error("Download (HTTP GET) failed with a connection error: %s" % (str(e)))

    def upload(self):

        try:
            if self.config.content is not None:
                ##  XXX: implement
                pass
            else:
                self.uploadRandom(
                    self.config.bytes,
                    self.config.minimum_gap,
                    self.config.chunk_size,
                )

        except (socket.error, httplib.HTTPException), e:
            log.error("Upload (HTTP POST) failed with an error: %s" % (str(e)))
            return

    def uploadRandom(self, bytes, min_gap, chunk_size):
        HTTP_DEVNULL = "/itt/testing/dev/null"

        ##  Do we have minimum packet gaps?
        gap = 0
        if min_gap is not None:
            gap = float(min_gap)

        ##  Do we have maximum chunk sizes?
        chunk = 0
        if chunk_size is not None:
            chunk = int(chunk_size)
        
        ##  Open HTTP connection & send headers
        http = self.setupUploadConnection(HTTP_DEVNULL)

        ##  Send data
        i = 0
        while int(i) < int(bytes):
            if chunk > 0:
                ##  Send only as much as we're allowed
                self.addAndSend(http, os.urandom(chunk))
                i = i + int(chunk)
                ##  Sleep for the minimum gap size
                time.sleep(gap)

            else:
                ##  Send everything as fast as possible
                self.addAndSend(http, os.urandom(bytes))
                i = i + bytes

        ##  XXX: todo: generalise the sha1sum stuff
        shasum = hashlib.sha1(self.sent_data).hexdigest()
        log.info("Sent %s bytes" % len(self.sent_data))
        log.info("SHA1 sum: %s" % shasum)

        ##  XXX: todo: if response ==200, else: error
        response = http.getresponse()
        log.info("Response status: %s" % (
            response.status,
        ))


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


    def run(self):

        ##  XXX: Replace with a configuration object
        parser = optparse.OptionParser(
            add_help_option=True,
            usage='%prog [options]',
            prog='itt.HttpClient',
        )

        parser.add_option('-u', '--url',
            default='http://localhost:8000/',
            help='URL to access [default: %default]')

        parser.add_option('-U', '--upload', action="store_true",
            default=False,
            help='Run an upload test (mutually exclusive to --download)')

        parser.add_option('-D', '--download', action="store_true",
            default=False,
            help='Run an download test (mutually exclusive to --upload)')

        (self.opts, args) = parser.parse_args()

        if len(args) != 0:
            log.warning("HTTP client takes no arguments, ignoring the ones provided")
        
        if self.opts.upload and self.opts.download:
            log.error("HTTP client can only upload _or_ download, not both")
        elif not self.opts.upload and not self.opts.download:
            log.error("HTTP client needs to be told to do an upload or a download")
        elif self.opts.download:
            self.download()
        elif self.opts.upload:
            self.upload()
        else:
            log.error("Something has gone horribly wrong")


if __name__ == '__main__':
    myClient = itt.HttpClient()
    myClient.run()
