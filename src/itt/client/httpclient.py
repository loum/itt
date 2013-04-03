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

import itt
from itt.utils.log import log, class_logging

class HttpClient(itt.Client):
    '''Provides a HTTP client for uploads & downloads
    '''

    def download(self):
        log.info("HTTP client begins download (HTTP GET): %s" % (self.opts.url))
        try:
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
        url_split = urlparse.urlsplit(self.opts.url)

        try:
            if url_split.netloc != '':
                http = httplib.HTTPConnection(url_split.netloc, timeout=20)     ##  Un-hardcode timeout?
            else:
                log.error("No hostname determined from URL, did you forget 'http://' ?")
                return

            http.putrequest("POST", url_split.path)
            http.putheader("content-type", "text/plain")    ##  Un-hardcore text/plain if needed?

            ##  A quick note why we don't provide content-length: because we
            ##  don't want to have to pre-calculate it.  We don't have to
            ##  worry about progress bars, so lets leave it.
            ##  See: http://tech.hickorywind.org/articles/2008/05/23/content-length-mostly-does-not-matter-the-reverse-bob-barker-rule
            ##  http.putheader("content-length", len(???))

            http.endheaders()
            http.send("crazy crazy crazy")
            time.sleep(1)
            http.send("crazy crazy crazy")

            ##  XXX: todo: generalise the sha1sum stuff
            shasum = hashlib.sha1("crazy crazy crazycrazy crazy crazy").hexdigest()
            log.info("SHA1 sum: %s" % shasum)

            ##  XXX: todo: if response ==200, else: error
            response = http.getresponse()
            log.info("Response status: %s" % (
                response.status,
            ))
        except (socket.error, httplib.HTTPException), e:
            log.error("Upload (HTTP POST) failed with an error: %s" % (str(e)))
            return


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
