from werkzeug.wrappers import Request, Response
import json
import re
from omsread import read_data

def application(environ, start_response):
    request = Request(environ)
    args = list(filter(bool, request.args.get('args', '').split(',')))
    data = json.dumps(read_data(args))
    print "args = ", args
    response = Response(data, mimetype='application/json')
    response.headers['Access-Control-Allow-Origin'] = 'null'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response(environ, start_response)

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('localhost', 8000, application)
