#!/usr/bin/env python

'''
@author: pjay
'''

##  Hack for running IttClient from itself; ie. ./ittclient.py
import sys
sys.path.insert(0, "../..")

import optparse
import time

import itt
from itt.utils.log import log, class_logging

class IttClient(object):
    '''Provides the ITT client for uploads & downloads via any protocol
    '''
    def __init__(self):
        self.upload = None
    
    def parse_args(self):
        ONE_MEGABYTE=1048576

        parser = optparse.OptionParser(
            add_help_option=True,
            usage='%prog [options]',
            prog='itt.IttClient',
        )

        parser.add_option('-D', '--direction',
            default='foo',
            help='Direction of test (upload [u, up], or, download [d, down])',
        )

        parser.add_option('-H', '--host',
            default='127.0.0.1',
            help='Host to connect to (either DNS name, or IP address)',
        )

        parser.add_option('-p', '--port',
            help='Port number to connect to on the host',
        )

        parser.add_option('-P', '--protocol',
            help='Protocol to use to transfer the content (HTTP, FTP, or TFTP)',
        )

        parser.add_option('-s', '--size',
            default=ONE_MEGABYTE,
            help='Size of the content to be sent in bytes (applicable to random content only) [default: %default]',
        )

        parser.add_option('-f', '--filename',
            default=None,
            help='File to upload or download (optional: if omitted, then random data will be used)',
        )

        parser.add_option('-g', '--minimum_gap',
            default=None,
            help='Minium gap between chunks (given in seconds)',
        )

        parser.add_option('-S', '--chunk_size',
            default=None,
            help='Size of data (in bytes) to be sent in a "chunk" (i.e. with no deliberate pauses)',
        )

        (self.opts, args) = parser.parse_args()

        if len(args) != 0:
            log.warning("ITT client takes no arguments, ignoring the ones provided")

        if self.opts.direction.lower() == 'u' or  \
           self.opts.direction.lower() == 'up' or \
           self.opts.direction.lower() == 'upload':
            self.upload = True
        elif self.opts.direction.lower() == 'd' or    \
             self.opts.direction.lower() == 'down' or \
             self.opts.direction.lower() == 'download':
            self.upload = False
        else:
            ##  XXX: Throw an ITT exception properly
            msg = "ITT client needs to be told to do an upload or a download"
            log.error(msg)
            raise Exception(msg)

        if self.opts.port is None:
            ##  XXX: Throw an ITT exception properly
            msg = "ITT client needs to be told a port number"
            log.error(msg)
            raise Exception(msg)

        if self.opts.filename is not None:
            ##  Size doesn't matter if filename is specified
            self.opts.size = None


    def get_test_config(self):
        config = itt.TestConfig(
            chunk_size=self.opts.chunk_size,
            minimum_gap=self.opts.minimum_gap,
        )
        return config

    def get_test_content(self):
        content = itt.TestContent(self.opts.filename,
            bytes=self.opts.size,
        )
        return content

    def get_test_connection(self):
        connection = itt.TestConnection(
            self.opts.host, self.opts.port, self.opts.protocol,
        )
        return connection

    def get_test_client(self, test):
        if test.connection.protocol == "http":
            client = itt.HttpClient(test)
        elif test.connection.protocol == "ftp":
            client = itt.FtpClient(test)
        elif test.connection.protocol == "tftp":
            client = itt.TftpClient(test)
        else:
            msg = "Invalid protocol"
            log.error(msg)
            raise Exception(msg)

        return client


if __name__ == '__main__':

    cliClient = IttClient()
    cliClient.parse_args()

    testConfig = cliClient.get_test_config()
    testContent = cliClient.get_test_content()
    testConnection = cliClient.get_test_connection()

    theTest = itt.Test(testConfig, testContent, testConnection)

    theClient = cliClient.get_test_client(theTest)
    
    if cliClient.upload:
        theClient.upload()
    else:
        theClient.download()
