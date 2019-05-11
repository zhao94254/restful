# -*- coding: utf-8 -*-
# @time: 2019-05-11 14:42
# @Author  : zpy
# @Email   : zpy94254@gmail.com
# @file: app.py

from flask import Flask, request
from flask_restful import Resource, Api, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


app = Flask(__name__)
api = Api(app)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=['1/day'],
)

todos = {}

def special_limit():
    tp =  request.args.get('type', None)
    if tp == 'vip':
        return '1/minute'
    elif tp == 'svip':
        return '1/second'
    else:
        return '1/day'

class TodoSimple(Resource):

    decorators = [ limiter.limit(special_limit,per_method=True, methods=['get'])]

    def get(self, todo_id=None):
        if todo_id:
            if todo_id not in todos:
                abort(404)
            return [{todo_id: todos[todo_id]}]
        else:
            return [todos]

    def post(self):
        todos[request.form['todo_id']] = request.form['data']
        return '', 201

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id : todos[todo_id]}

    def delete(self, todo_id):
        todos.pop(todo_id)
        return '', 204


api.add_resource(TodoSimple, '/todo', '/todo/<string:todo_id>')

if __name__ == '__main__':
    app.run(debug=True)
