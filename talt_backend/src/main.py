from config import HTTP_PORT, CACHE_TIMEOUT, logger
from flask import Flask, request
from flask import jsonify
from flask_caching import Cache
from flask_restplus import Resource, Api, fields, reqparse

import data_item

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
class Ping(Resource):
    # @cache.cached(timeout=CACHE_TIMEOUT)
    def get(self):
        args = request.args
        logger.debug(args)
        args_list = [":".join(item) for item in args.items()]
        return "pong with {}".format(str(", ".join(args_list)))


@api.route("/data/save_one")
class DataSaveOne(Resource):
    def post(self):
        json_data = request.json
        if 'payload' in json_data:
            payload = json_data['payload']
            logger.debug(payload)
            #TODO Handle quality checking and save to db.
            item = payload
            data_item.save_item(item)
            return "Not today."
        else:
            logger.warning("No payload in post json data.")
            return "Not here."


@api.route("/data/get_one")
class DataSaveOne(Resource):
    def get(self):
        args = request.args
        logger.debug(args)
        #TODO Handle get one data item to be label and review and send to frontend.

        dump_data = {
            "_id": "fake00001"
            , "type": "text"
            , "data": {
                "content": "This is a item to be label."
                , "class": "testing"
                , "tags": [
                    "testing"
                ]
            }
        }
        return jsonify(dump_data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=HTTP_PORT, threaded=True)
