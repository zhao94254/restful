# -*- coding: utf-8 -*-
# @time: 2019-05-11 15:23
# @Author  : zpy
# @Email   : zpy94254@gmail.com
# @file: testapp.py

import requests

burl = 'http://localhost:5000/'

import unittest

from flask_testing import TestCase


class ApiTest(unittest.TestCase):



    def test_todopost(self):
        resp = requests.post(f'{burl}todo', data={'user': 'test','data': 'test'})
        assert resp.status_code == 201

    def test_todoget(self):
        resp = requests.get(f'{burl}todo?user=test&type=svip')
        assert resp.status_code == 200
        assert resp.status_code in (200, 404)

    def test_todoput(self):
        ndata = 'test'
        _id = requests.get(f'{burl}todo?user=test&type=svip').json()[0]['_id']
        resp = requests.put(f'{burl}todo/{_id}', data={'data': ndata})
        assert resp.status_code == 200
        assert resp.json()['1'] == ndata

    def test_tododelete(self):
        _id = requests.get(f'{burl}todo?user=test&type=svip').json()[0]['_id']
        resp = requests.delete(f'{burl}todo/{_id}')
        assert resp.status_code == 204


if __name__ == '__main__':
    unittest.main()
