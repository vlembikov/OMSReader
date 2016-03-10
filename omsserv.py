from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import json
from omsread import read_data

class HttpProcessor(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('content-type','application/json')
        self.send_header('Access-Control-Allow-Origin', 'null')
        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.end_headers()
        da = read_data()
        d = json.dumps(da) 
        self.wfile.write(d)
server_address = ("", 8000)
httpd = HTTPServer(server_address, HttpProcessor)
httpd.serve_forever()
