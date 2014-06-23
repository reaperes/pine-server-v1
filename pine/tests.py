import re
import json
from urllib import parse

from django.test import TestCase
from django.test.client import Client
from django.test.client import RequestFactory
from django.conf import settings

from pine.pine import Protocol

URL = '/threads'


class UnitThreadTestCase(TestCase):
    fixtures = ['users.json', 'threads.json']

    def setUp(self):
        self.factory = RequestFactory()

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
        self.image_path = settings.BASE_DIR + '/resources/png_sample.png'

    def test_post_friends_thread(self):
        c = Client()
        response = None
        with open(settings.BASE_DIR + '/resources/png_sample.png', 'rb') as fp:
            j = {
                'json': json.dumps(self.post_friend_thread_json),
                'bg_image_file': fp
            }
            response = c.post(URL, j).content.decode('utf-8')
            response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

    def test_get_friends_thread(self):
        c = Client()
        uri = parse.urlencode(self.get_friend_threads_json)
        response = c.get(URL+'?'+uri, content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
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

    def test_get_valid_content_after_post_friend_thread(self):
        c = Client()
        response = None
        with open(settings.BASE_DIR + '/resources/png_sample.png', 'rb') as fp:
            j = {
                'json': json.dumps(self.post_friend_thread_json),
                'bg_image_file': fp
            }
            response = c.post(URL, j).content.decode('utf-8')
            response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

        uri = parse.urlencode(self.get_friend_threads_json)
        response = c.get(URL+'?'+uri, content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        assert response[Protocol.DATA][0]['content'] == 'post_friend_thread_json'
        assert re.search(r'.*png_sample\.png.*', response[Protocol.DATA][0]['image_url'])
