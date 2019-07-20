from config import HTTP_PORT, CACHE_TIMEOUT, logger
from flask import Flask, request
from flask import jsonify
from flask_caching import Cache
from flask_restplus import Resource, Api, fields, reqparse

app = Flask(__name__)
api = Api(app, version='0.1', title='TALT BACKEND API', doc='/docs')
cache = Cache(app, config={'CACHE_TYPE': 'simple'})


def exit_handler():
    '''
    #DEPRECATED
    do_something()
    '''
    pass


def startup_handler():
    '''
    do_something()
    '''
    pass


@api.route("/ping")
class questions(Resource):
    # @cache.cached(timeout=CACHE_TIMEOUT)
    def get(self):
        args = request.args
        logger.debug(args)
        return "pong with {}".format(str(", ".join(args)))


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=HTTP_PORT, threaded=True)
