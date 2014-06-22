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
        print(response)

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
        print(response.content)

# def send_request(data={}, method='POST', url=URL):
#     if method is 'POST':
#         c = Client()
#         response = c.post(url, content_type='application/json', data=json.dumps(send_object)).content.decode('utf-8')
#         return json.loads(response)
#
#     elif method is 'GET':
#         c = Client()
#         uri = parse.urlencode(send_object)
#         response = c.get(url+'?'+uri, content_type='application/json').content.decode('utf-8')
#         return json.loads(response)
