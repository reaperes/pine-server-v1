import re
import json
from urllib import parse

from django.test import TestCase
from django.test.client import Client
from django.test.client import RequestFactory
from django.conf import settings

from pine.pine import Protocol

URL = '/users'


class UnitThreadTestCase(TestCase):
    fixtures = ['users.json', 'threads.json']

    def setUp(self):
        self.post_block_user_json = {
            'user': 9
        }

    def test_post_friends_thread_with_image(self):
        c = Client()
        response = c.post(URL+'/2/block', data=json.dumps(self.post_block_user_json),
                          content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS


class IntegrationThreadTestCase(TestCase):
    fixtures = ['users.json', 'threads.json']

    def setUp(self):
        self.get_friend_threads_json = {
            'user': 1,
            'is_friend': True,
            'offset': 0,
            'limit': 1
        }
        self.post_block_user_json = {
            'user': 1
        }
        self.post_friend_thread_json = {
            'author': 2,
            'is_public': False,
            'content': 'post_friend_thread_json2'
        }

    def test_get_no_content_from_user2_after_user2_blocked(self):
        c = Client()
        uri = parse.urlencode(self.get_friend_threads_json)
        response = c.get('/threads?' + uri, content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

        before_content = response[Protocol.DATA][0]['content']
        response = c.post(URL+'/2/block', data=json.dumps(self.post_block_user_json),
                          content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

        response = c.post('/threads', data=json.dumps(self.post_friend_thread_json),
                          content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

        response = c.get('/threads?' + uri, content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        assert not response[Protocol.DATA][0]['content'] == 'post_friend_thread_json2'
        assert before_content == response[Protocol.DATA][0]['content']
