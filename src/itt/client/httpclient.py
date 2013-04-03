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

import itt
from itt.utils.log import log, class_logging

class HttpClient(itt.Client):
    '''Provides a HTTP client for uploads & downloads
    '''

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
        
        (self.opts, args) = parser.parse_args()

        if len(args) != 0:
            log.warning("HTTP client takes no arguments, ignoring the ones provided")
        
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

if __name__ == '__main__':
    myClient = itt.HttpClient()
    myClient.run()
