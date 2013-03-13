'''
Created on Mar 13, 2013

@author: pjay
'''

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
        
        url = 'http://127.0.0.1:8000/fast/'
        print time.asctime(), "XXX: Client begins download - %s" % (url)
        download = requests.get(url)
        print time.asctime(), "XXX: Client finishes download - %s" % (url)
 
        if download.status_code == 200:
            shasum = hashlib.sha1(download.content).hexdigest()
            print time.asctime(), "XXX: SHA1 sum of content received - %s" % (shasum)
            
        
            
        
    
if __name__ == '__main__':
    myClient = IttHttpClient()
    myClient.run()