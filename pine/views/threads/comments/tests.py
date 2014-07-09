import re
import json
from urllib import parse

from django.test import TestCase
from django.test.client import Client
from django.test.client import RequestFactory
from django.conf import settings

from pine.pine import Protocol


class UnitThreadTestCase(TestCase):
    fixtures = ['users.json', 'threads.json', 'comments.json']

    def setUp(self):
        self.get_thread_comments_json = {
            'user': 1
        }
        self.post_thread_comment_json = {
            'user': 1,
            'content': 'Hello, world.'
        }

    def test_get_thread_comment(self):
        c = Client()
        uri = parse.urlencode(self.get_thread_comments_json)
        response = c.get('/threads/1/comments?'+uri).content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        assert response[Protocol.DATA][0]['comment_user_id'] == 0
        assert response[Protocol.DATA][1]['comment_user_id'] == 1
        assert response[Protocol.DATA][0]['likes'] == 3
        assert response[Protocol.DATA][1]['likes'] == 0
        assert response[Protocol.DATA][0]['is_user_like'] is True
        assert response[Protocol.DATA][1]['is_user_like'] is False
        assert response[Protocol.DATA][0]['comment_type'] == 3
        assert response[Protocol.DATA][1]['comment_type'] == 0

        self.get_thread_comments_json['user'] = 4
        uri = parse.urlencode(self.get_thread_comments_json)
        response = c.get('/threads/1/comments?'+uri).content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.DATA][0]['comment_type'] == 2
        assert response[Protocol.DATA][2]['comment_type'] == 1
        assert response[Protocol.DATA][2]['comment_user_id'] == 2

    def test_post_thread_comment(self):
        c = Client()
        response = c.post('/threads/1/comments',
                          data=json.dumps(self.post_thread_comment_json),
                          content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS


class IntegrationThreadTestCase(TestCase):
    fixtures = ['users.json', 'threads.json', 'comments.json']

    def test_get_thread_comment_after_post_thread_comment(self):
        get_thread_comments_json = {
            'user': 1
        }
        c = Client()
        uri = parse.urlencode(get_thread_comments_json)
        response = json.loads(c.get('/threads/2/comments?' + uri).content.decode('utf-8'))
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        assert len(response[Protocol.DATA]) == 0

        post_thread_comment_json = {
            'user': 1,
            'content': 'Hello, world.'
        }
        response = c.post('/threads/2/comments',
                          data=json.dumps(post_thread_comment_json),
                          content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

        response = json.loads(c.get('/threads/2/comments?' + uri).content.decode('utf-8'))
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        assert len(response[Protocol.DATA]) == 1
