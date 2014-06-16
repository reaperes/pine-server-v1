from django.test import TestCase
from django.test.client import Client
import json

from pine.pine import Protocol
from pine.views import ErrorMessage


URL = '/threads'


class PostThreadTestCase(TestCase):
    def setUp(self):
        self.post_thread_json = {
            'author': '123456789012345',
            'content': 'Hello, Test content'
        }
        self.get_threads_json = {
            'offset': 0,
            'limit': 1
        }

    def test_valid_post(self):
        response = send_data(self.post_thread_json)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

    def test_valid_post_max_character_content(self):
        self.post_thread_json['content'] = '1234567890' * 20    # 200 length content
        response = send_data(self.post_thread_json)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

    def test_invalid_post_no_author(self):
        self.post_thread_json.__delitem__('author')
        response = send_data(self.post_thread_json)
        assert response[Protocol.RESULT] == Protocol.FAIL
        assert response[Protocol.MESSAGE] == ErrorMessage.POST_MALFORMED_AUTHOR

    def test_invalid_post_too_long_author(self):
        self.post_thread_json['author'] = '1234567890123456'
        response = send_data(self.post_thread_json)
        assert response[Protocol.RESULT] == Protocol.FAIL
        assert response[Protocol.MESSAGE] == ErrorMessage.POST_MALFORMED_AUTHOR

    def test_invalid_post_no_content(self):
        self.post_thread_json.__delitem__('content')
        response = send_data(self.post_thread_json)
        assert response[Protocol.RESULT] == Protocol.FAIL
        assert response[Protocol.MESSAGE] == ErrorMessage.POST_MALFORMED_CONTENT

    def test_invalid_post_too_long_content(self):
        self.post_thread_json['content'] = '1234567890' * 20 + '1'  # 201 length content
        response = send_data(self.post_thread_json)
        assert response[Protocol.RESULT] == Protocol.FAIL
        assert response[Protocol.MESSAGE] == ErrorMessage.POST_MALFORMED_CONTENT


class GetThreadsTestCase(TestCase):
    def setUp(self):
        self.post_thread_json = {
            'author': '123456789012345',
            'content': 'Hello, Test content'
        }
        self.get_threads_json = {
            'offset': 0,
            'limit': 1
        }

    def test_valid_get_threads(self):
        response = send_data(self.post_thread_json)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

        self.post_thread_json['content'] = '1234567890' * 20
        response = send_data(self.post_thread_json)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

        response = send_data(self.get_threads_json, method='GET', url=URL+r'?offset=0&limit=10')
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        assert len(response[Protocol.DATA]) == 2

    def test_invalid_get_threads_offset_10000(self):
        response = send_data(self.get_threads_json, method='GET', url=URL+r'?offset=10000&limit=10')
        assert response[Protocol.RESULT] == Protocol.FAIL
        assert response[Protocol.MESSAGE] == ErrorMessage.GET_MALFORMED_OFFSET

    def test_invalid_get_threads_offset_no_number(self):
        response = send_data(self.get_threads_json, method='GET', url=URL+r'?offset=a&limit=10')
        assert response[Protocol.RESULT] == Protocol.FAIL
        assert response[Protocol.MESSAGE] == ErrorMessage.GET_MALFORMED_OFFSET

    def test_invalid_get_threads_limit_101(self):
        response = send_data(self.get_threads_json, method='GET', url=URL+r'?offset=200&limit=101')
        assert response[Protocol.RESULT] == Protocol.FAIL
        assert response[Protocol.MESSAGE] == ErrorMessage.GET_MALFORMED_LIMIT

    def test_invalid_get_threads_limit_no_number(self):
        response = send_data(self.get_threads_json, method='GET', url=URL+r'?offset=100&limit=c')
        assert response[Protocol.RESULT] == Protocol.FAIL
        assert response[Protocol.MESSAGE] == ErrorMessage.GET_MALFORMED_LIMIT


def send_data(send_object, method='POST', url=URL):
    if method is 'POST':
        c = Client()
        response = c.post(url, content_type='application/json', data=json.dumps(send_object)).content.decode('utf-8')
        return json.loads(response)

    elif method is 'GET':
        c = Client()
        response = c.get(url, content_type='application/json').content.decode('utf-8')
        return json.loads(response)
