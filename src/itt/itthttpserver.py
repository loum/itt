"""
Created on Mar 6, 2013

@author: pjay
"""

import time
import BaseHTTPServer

HOST_NAME = ''
PORT_NUMBER = 8000

class IttHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """
    classdocs
    """
    
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
    def do_GET(self):
        """Respond to a GET request."""
        path_array = self.path.split('/')
        
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        
        self.wfile.write("Selected path %s\n" % path_array[1])
        
        if path_array[1] == 'fast':
            self.wfile.write("Fastest possible transfer *\n")
            self.wfile.write("* as limited by the TCP stack & network\n")
            self.wfile.flush()
            for i in range(1000):
                self.wfile.write("Line #%s / 1000\n" % i)
            self.wfile.flush()

        elif path_array[1] == 'slow':
            self.wfile.write("Slow transfer *\n")
            self.wfile.write("* a few bytes every 1 second\n")
            self.wfile.flush()
            for i in range(1000):
                self.wfile.write("Line #%s / 1000\n" % i)
                time.sleep(1)
                self.wfile.flush()
                
        else:
            self.wfile.write("You chose %s, which is not valid\n" % path_array[1])
            self.wfile.write("Try fast or slow\n")
            self.wfile.flush()
            
if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class(('', PORT_NUMBER), IttHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)