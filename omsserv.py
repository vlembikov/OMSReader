from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import cgi
import json
from omsread import read_data

class HttpProcessor(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.send_header('content-type','application/json')
        self.send_header('Access-Control-Allow-Origin', 'null')
        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.end_headers()
        args = None
        da = read_data(args)
        d = json.dumps(da) 
        self.wfile.write(d)
    def do_GET(self):
        self.send_response(200)
        self.send_header('content-type','application/json')
        self.send_header('Access-Control-Allow-Origin', 'null')
        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.end_headers()
        args = None
        da = read_data(args)
        d = json.dumps(da) 
        self.wfile.write(d)
server_address = ("", 8000)
httpd = HTTPServer(server_address, HttpProcessor)
print "serving at ", server_address
print "Press CTRL+C for ending"
httpd.serve_forever()
