#!/usr/bin/env python

'''
@author: pjay
'''

##  Hack for running IttClient from itself; ie. ./ittclient.py
import sys
sys.path.insert(0, "../..")

import optparse
import time

from types import *

import itt
from itt.utils.log import log, class_logging

class IttClient(object):
    '''Provides the ITT client for uploads & downloads via any protocol
    '''
    def __init__(self):
        self.upload = None
    
    def parseArgs(self):
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

        parser.add_option('-c', '--content',
            default=None,
            help='Content to upload or download (optional: if omitted, then random content will be used)',
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

        if type(self.opts.port) is NoneType:
            ##  XXX: Throw an ITT exception properly
            msg = "ITT client needs to be told a port number"
            log.error(msg)
            raise Exception(msg)

        if self.opts.content is not None:
            ##  Size doesn't matter if content is specified
            self.opts.size = None


    def getTestConfig(self):
        config = itt.TestConfig(
            self.opts.host, self.opts.port, self.opts.protocol,
            upload=self.upload,
            bytes=self.opts.size,
            content=self.opts.content,
            chunk_size=self.opts.chunk_size,
            minimum_gap=self.opts.minimum_gap,
        )
        return config


    def getTestClient(self, config):
        if config.protocol == "http":
            client = itt.HttpClient(config)
        elif config.protocol == "ftp":
            client = itt.FtpClient()
        elif config.protocol == "tftp":
            client = itt.TftpClient()
        else:
            msg = "Invalid protocol"
            log.error(msg)
            raise Exception(msg)

        return client


if __name__ == '__main__':

    myClient = IttClient()
    myClient.parseArgs()

    testConfig = myClient.getTestConfig()

    testClient = myClient.getTestClient(testConfig)
    
    if testConfig.upload:
        testClient.upload()
    else:
        testClient.download()
