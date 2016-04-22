#!/usr/bin/python

import json
import sys
import os
import argparse
from omsread import read_data
sys.path.insert(0, os.path.join(sys.path[0], 'lib'))
from werkzeug.wrappers import Request, Response

def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-p', '--port', default=5050)
    return parser

def application(environ, start_response):
    request = Request(environ)
    args = list(filter(bool, request.args.get('args', '').split(',')))
    data = json.dumps(read_data(args))
    response = Response(data, mimetype='application/json')
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response(environ, start_response)

if __name__ == '__main__':
    parser = createParser()
    portserv = parser.parse_args(sys.argv[1:])
    from werkzeug.serving import run_simple
    run_simple('localhost', portserv.port, application)
