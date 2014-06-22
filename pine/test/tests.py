import json
from urllib import parse

from django.test import TestCase
from django.test.client import Client

from pine.pine import Protocol

URL = '/test'


class CoreTestCase(TestCase):
    def test_post_request_mirror(self):
        request_json = {
            'integer_0': 0,
            'integer_1': 1,
            'integer_minus_1': -1,
            'boolean_true': True,
            'boolean_false': False,
            'string_a': 'a',
            'string_true': 'true',
            'string_false': 'false',
            'string_0': '0',
            'string_1': '1'
        }

        c = Client()
        response = c.post(URL, content_type='application/json', data=json.dumps(request_json)).content.decode('utf-8')
        # print(response)

    def test_get_request_mirror(self):
        request_json = {
            'integer_0': 0,
            'integer_1': 1,
            'integer_minus_1': -1,
            'boolean_true': True,
            'boolean_false': False,
            'string_a': 'a',
            'string_true': 'true',
            'string_false': 'false',
            'string_0': '0',
            'string_1': '1'
        }

        c = Client()
        uri = parse.urlencode(request_json)
        response = c.get(URL+'?'+uri)
        # print(response)
