"""
Created on Mar 6, 2013

@author: pjay
"""

import time
import hashlib
import BaseHTTPServer

class IttHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """
    classdocs
    """
    
    contentSent = ''
    
    def storeAndWrite(self, str, wfile):
        """Store the string in self.contentSent, and write it to wfile)"""
        self.contentSent = self.contentSent + str
        wfile.write(str)
    
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
    def do_GET(self):
        """Respond to a GET request."""
        print time.asctime(), "XXX: GET request received from %s on port %s for %s" % (
           self.client_address[0],
           self.client_address[1],
           self.path,
        )
        
        path_array = self.path.split('/')
        
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        
        self.storeAndWrite(("Selected path %s\n" % path_array[1]), self.wfile)
        
        if path_array[1] == 'fast':
            self.storeAndWrite(("Fastest possible transfer *\n"), self.wfile)
            self.storeAndWrite(("* as limited by the TCP stack & network\n"), self.wfile)
            self.wfile.flush()
            for i in range(1000):
                self.storeAndWrite(("Line #%s / 1000\n" % i), self.wfile)
            self.wfile.flush()

        elif path_array[1] == 'slow':
            self.storeAndWrite(("Slow transfer *\n"), self.wfile)
            self.storeAndWrite(("* a few bytes every 1 second\n"), self.wfile)
            self.wfile.flush()
            for i in range(10):
                self.storeAndWrite(("Line #%s / 1000\n" % i), self.wfile)
                time.sleep(1)
                self.wfile.flush()
                
        else:
            self.storeAndWrite(("You chose %s, which is not valid\n" % path_array[1]), self.wfile)
            self.storeAndWrite(("Try fast or slow\n"), self.wfile)
            self.wfile.flush()
            
        print time.asctime(), "XXX: GET request finished for %s on port %s for %s" % (
           self.client_address[0],
           self.client_address[1],
           self.path,
        )
        shasum = hashlib.sha1(self.contentSent).hexdigest()
        print time.asctime(), "XXX: SHA1 sum of content send to %s on port %s is: %s" % (
           self.client_address[0],
           self.client_address[1],
           shasum,
        )

class IttHttpServer:
    
    def run(self, bind='', port=8000):    
        server_class = BaseHTTPServer.HTTPServer
        httpd = server_class((bind, port), IttHandler)
            
        print time.asctime(), "XXX: Server Starts - %s:%s" % (bind, port)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()
        print time.asctime(), "XXX: Server Stops - %s:%s" % (bind, port)
    
if __name__ == '__main__':
    myServer = IttHttpServer()
    myServer.run()