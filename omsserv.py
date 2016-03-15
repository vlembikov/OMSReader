from werkzeug.wrappers import Request, Response
import json
from omsread import read_data

def application(environ, start_response):
    request = Request(environ)
    args = request.args.get('args')
    if args:
        data = json.dumps(read_data(str(args)))
    else:
        data = json.dumps(read_data(args))
    print "args = ", args
    response = Response(data, mimetype='application/json')
    response.headers['Access-Control-Allow-Origin'] = 'null'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response(environ, start_response)

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('localhost', 8000, application)
