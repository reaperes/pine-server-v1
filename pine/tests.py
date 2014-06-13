from django.test import TestCase
from django.test.client import Client
import json

from pine.pine import Protocol
from pine.views import ErrorMessage


URL = '/thread/post'


class ThreadTestCase(TestCase):
    default_json = {}

    def setUp(self):
        self.default_json = {
            'author': '123456789012345',
            'content': 'Hello, Test content'
        }
        pass

    def test_valid_post(self):
        response = post_data(self.default_json)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

    def test_invalid_post_no_author(self):
        self.default_json.__delitem__('author')
        response = post_data(self.default_json)
        assert response[Protocol.RESULT] == Protocol.FAIL
        assert response[Protocol.MESSAGE] == ErrorMessage.MALFORMED_AUTHOR

    def test_invalid_post_too_long_author(self):
        self.default_json['author'] = '1234567890123456'
        response = post_data(self.default_json)
        assert response[Protocol.RESULT] == Protocol.FAIL
        assert response[Protocol.MESSAGE] == ErrorMessage.MALFORMED_AUTHOR

    def test_invalid_post_no_content(self):
        self.default_json.__delitem__('content')
        response = post_data(self.default_json)
        assert response[Protocol.RESULT] == Protocol.FAIL
        assert response[Protocol.MESSAGE] == ErrorMessage.MALFORMED_CONTENT

    def test_valid_post_max_character_content(self):
        self.default_json['content'] = '1234567890' * 20    # 200 length content
        response = post_data(self.default_json)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

    def test_invalid_post_too_long_content(self):
        self.default_json['content'] = '1234567890' * 20 + '1'  # 201 length content
        response = post_data(self.default_json)
        assert response[Protocol.RESULT] == Protocol.FAIL
        assert response[Protocol.MESSAGE] == ErrorMessage.MALFORMED_CONTENT


def post_data(send_object):
    c = Client()
    response = c.post(URL, content_type='application/json', data=json.dumps(send_object)).content.decode('utf-8')
    return json.loads(response)
