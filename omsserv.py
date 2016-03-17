from lib.werkzeug.wrappers import Request, Response
import json
import sys
import argparse
from omsread import read_data

def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-p', '--port', default=8000)
    return parser

def application(environ, start_response):
    request = Request(environ)
    args = list(filter(bool, request.args.get('args', '').split(',')))
    data = json.dumps(read_data(args))
    response = Response(data, mimetype='application/json')
    response.headers['Access-Control-Allow-Origin'] = 'null'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response(environ, start_response)

if __name__ == '__main__':
    parser = createParser()
    portserv = parser.parse_args(sys.argv[1:])
    from werkzeug.serving import run_simple
    run_simple('localhost', portserv.port, application)
