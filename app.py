# -*- coding: utf-8 -*-
# @time: 2019-05-11 14:42
# @Author  : zpy
# @Email   : zpy94254@gmail.com
# @file: app.py

from flask import Flask, request
from flask_restful import Resource, Api, abort, reqparse, fields, marshal_with
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import pymongo
from pymongo.bulk import ObjectId
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
mongo_client = pymongo.MongoClient()
app = Flask(__name__)
api = Api(app)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=['1/day'],
)


def special_limit():
    tp =  request.args.get('type', None)
    if tp == 'vip':
        return '1/minute'
    elif tp == 'svip':
        return '30/second'
    else:
        return '1/day'


class APISchema():
    """describes input and output formats for resources,
    and parser deals with arguments to the api.
    """
    get_fields = {
        'id': fields.Integer,
        'created': fields.DateTime(dt_format='iso8601')
    }

    def __init__(self):
        self.parser = reqparse.RequestParser()

    def parse_args(self):
        return self.parser.parse_args()


class TodoSchema(APISchema):

    todo_fields = {
        'user': fields.String,
        'data': fields.String,
        '_id': fields.String
    }





class Todo(Resource):
    schema = TodoSchema()
    decorators = [auth.login_required, limiter.limit(special_limit,per_method=True, methods=['get'])]

    @marshal_with(schema.todo_fields)
    def get(self):
        user = request.args.get('user', None)
        if user:
            return list(mongo_client['test']['todo'].find({'user': user}))
        else:
            return []

    def post(self):
        mongo_client['test']['todo'].insert({
            'user': request.form['user'],
            'data': request.form['data']
        })

        return '', 201

    @marshal_with(schema.todo_fields)
    def put(self, todo_id):
        resp = mongo_client['test']['todo'].find_one_and_update({'_id': ObjectId(todo_id)}, {"$set":{"data": request.form['data']}})
        return resp

    def delete(self, todo_id):
        mongo_client['test']['todo'].delete_one({'_id': ObjectId(todo_id)})
        return '', 204


api.add_resource(Todo, '/todo', '/todo/<string:todo_id>')

if __name__ == '__main__':
    app.run(debug=True)
