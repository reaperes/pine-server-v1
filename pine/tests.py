import json
from urllib import parse

from django.test import TestCase
from django.test.client import Client

from pine.pine import Protocol

URL = '/threads'


class UnitThreadTestCase(TestCase):
    fixtures = ['users.json', 'threads.json']

    def setUp(self):
        self.post_friend_thread_json = {
            'author': 2,
            'is_public': False,
            'content': 'Hello, Test content'
        }
        self.post_public_thread_json = {
            'author': 2,
            'is_public': True,
            'content': 'Hello, Test content'
        }
        self.get_friend_threads_json = {
            'user': 2,
            'is_friend': True,
            'offset': 0,
            'limit': 1
        }
        self.get_public_threads_json = {
            'user': 2,
            'is_friend': False,
            'offset': 0,
            'limit': 1
        }

    def test_post_friends_thread(self):
        response = send_data(self.post_friend_thread_json)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

    def test_post_public_thread(self):
        response = send_data(self.post_public_thread_json)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

    def test_get_friends_threads(self):
        response = send_data(self.get_friend_threads_json, method='GET')
        assert response[Protocol.RESULT] == Protocol.SUCCESS

    def test_get_public_threads(self):
        response = send_data(self.get_public_threads_json, method='GET')
        assert response[Protocol.RESULT] == Protocol.SUCCESS


class IntegrationThreadTestCase(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.post_friend_thread_json = {
            'author': 1,
            'is_public': False,
            'content': 'post_friend_thread_json'
        }
        self.get_friend_threads_json = {
            'user': 2,
            'is_friend': True,
            'offset': 0,
            'limit': 1
        }
        self.post_public_thread_json = {
            'author': 1,
            'is_public': False,
            'content': 'post_public_thread_json'
        }
        self.get_public_threads_json = {
            'user': 2,
            'is_friend': False,
            'offset': 0,
            'limit': 1
        }

    def test_get_valid_content_after_post_friend_thread(self):
        response = send_data(self.post_friend_thread_json)
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        response = send_data(self.get_friend_threads_json, method='GET')
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        assert response[Protocol.DATA][0]['content'] == 'post_friend_thread_json'

    def test_get_valid_content_after_post_public_thread(self):
        response = send_data(self.post_public_thread_json)
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        response = send_data(self.get_friend_threads_json, method='GET')
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        assert response[Protocol.DATA][0]['content'] == 'post_public_thread_json'


def send_data(send_object, method='POST', url=URL):
    if method is 'POST':
        c = Client()
        response = c.post(url, content_type='application/json', data=json.dumps(send_object)).content.decode('utf-8')
        return json.loads(response)

    elif method is 'GET':
        c = Client()
        uri = parse.urlencode(send_object)
        response = c.get(url+'?'+uri, content_type='application/json').content.decode('utf-8')
        return json.loads(response)
