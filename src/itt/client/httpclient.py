#!/usr/bin/env python

'''
Created on Mar 13, 2013

@author: pjay
'''
import argparse
import requests
import hashlib
import time

class IttHttpClient():
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''

    def run(self):
        ## Read config!
        
        parser = argparse.ArgumentParser(description='ITT HTTP Test Client.')
        parser.add_argument('-u','--url')
        args = parser.parse_args()
        
        print time.asctime(), "XXX: Client begins download - %s" % (args.url)
        download = requests.get(args.url)
        print time.asctime(), "XXX: Client finishes download - %s" % (args.url)
 
        if download.status_code == 200:
            shasum = hashlib.sha1(download.content).hexdigest()
            print time.asctime(), "XXX: SHA1 sum of content received - %s" % (shasum)
            
        
            
        
    
if __name__ == '__main__':
    myClient = IttHttpClient()
    myClient.run()