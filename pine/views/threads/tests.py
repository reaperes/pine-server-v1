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

        self.get_thread = {
            'user': 2
        }

        self.get_friend_thread_offset = {
            'user': 2,
            'is_friend': True
        }

        self.get_public_thread_offset = {
            'user': 2,
            'is_friend': False
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

        self.post_thread_like_json = {
            'user': 1
        }

        self.post_thread_unlike_json = {
            'user': 2
        }

        self.post_report_thread_json = {
            'user': 2
        }

        self.post_block_thread_json = {
            'user': 2
        }

    def test_post_friends_thread_with_image(self):
        c = Client()
        response = None
        with open(settings.BASE_DIR + '/resources/jpeg_sample.jpeg', 'rb') as fp:
            j = {
                'json': json.dumps(self.post_friend_thread_json),
                'bg_image_file': fp
            }
            response = c.post(URL, j).content.decode('utf-8')
            response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

    def test_post_friends_thread_no_image(self):
        c = Client()
        response = c.post(URL,
                          data=json.dumps(self.post_friend_thread_json),
                          content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

    def test_get_thread(self):
        c = Client()
        uri = parse.urlencode(self.get_thread)
        response = c.get(URL+'/1?'+uri, content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        assert response[Protocol.DATA]['id'] == 1

    def test_get_friend_thread_offset(self):
        c = Client()
        uri = parse.urlencode(self.get_friend_thread_offset)
        response = c.get(URL+'/1/offset?'+uri, content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        assert response['offset'] == 1

    def test_get_public_thread_offset(self):
        c = Client()
        uri = parse.urlencode(self.get_public_thread_offset)
        response = c.get(URL+'/2/offset?'+uri, content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        assert response['offset'] == 3

    def test_get_friends_thread(self):
        c = Client()
        uri = parse.urlencode(self.get_friend_threads_json)
        response = c.get(URL+'?'+uri, content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

    def test_post_thread_like(self):
        c = Client()
        response = c.post(URL+'/8/like',
                          data=json.dumps(self.post_thread_like_json),
                          content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

    def test_post_thread_unlike(self):
        c = Client()
        response = c.post(URL+'/2/unlike',
                          data=json.dumps(self.post_thread_unlike_json),
                          content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

    def test_post_report_thread(self):
        c = Client()
        response = c.post(URL+'/7/report', data=json.dumps(self.post_report_thread_json),
                          content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

    def test_block_thread(self):
        c = Client()
        response = c.post(URL+'/5/block', data=json.dumps(self.post_block_thread_json),
                          content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS


class IntegrationThreadTestCase(TestCase):
    fixtures = ['users.json', 'threads.json']

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
        self.post_thread_like_json = {
            'user': 1
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

    def test_get_valid_content_after_post_friend_thread_no_image(self):
        c = Client()
        response = c.post(URL,
                          data=json.dumps(self.post_friend_thread_json),
                          content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

        uri = parse.urlencode(self.get_friend_threads_json)
        response = c.get(URL+'?'+uri, content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        assert response[Protocol.DATA][0]['content'] == 'post_friend_thread_json'
        assert response[Protocol.DATA][0]['image_url'] == ''

    def test_get_post_like_count_after_post_thread_like(self):
        c = Client()
        get_threads_json = {
            'user': 1,
            'is_friend': True,
            'offset': 0,
            'limit': 1
        }
        uri = parse.urlencode(get_threads_json)
        response = c.get(URL+'?'+uri, content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        assert response[Protocol.DATA][0]['is_user_like'] is False
        assert response[Protocol.DATA][0]['like'] == 7

        response = c.post(URL+'/8/like',
                          data=json.dumps(self.post_thread_like_json),
                          content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

        response = c.get(URL+'?'+uri, content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        assert response[Protocol.DATA][0]['is_user_like'] is True
        assert response[Protocol.DATA][0]['like'] == 8

    def test_get_post_like_count_after_post_thread_unlike(self):
        c = Client()
        get_threads_json = {
            'user': 1,
            'is_friend': True,
            'offset': 0,
            'limit': 1
        }
        uri = parse.urlencode(get_threads_json)
        response = c.get(URL+'?'+uri, content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        assert response[Protocol.DATA][0]['is_user_like'] is False
        assert response[Protocol.DATA][0]['like'] == 7

        self.post_thread_unlike_json = {
            'user': 2
        }
        response = c.post(URL+'/8/unlike',
                          data=json.dumps(self.post_thread_unlike_json),
                          content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

        response = c.get(URL+'?'+uri, content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        assert response[Protocol.DATA][0]['is_user_like'] is False
        assert response[Protocol.DATA][0]['like'] == 6

    def test_get_thread_after_post_report_thread(self):
        c = Client()
        get_threads_json = {
            'user': 2,
            'is_friend': True,
            'offset': 0,
            'limit': 1
        }
        uri = parse.urlencode(get_threads_json)
        response = c.get(URL+'?'+uri, content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        report_thread_id = response[Protocol.DATA][0]['id']

        self.post_report_thread_json = {
            'user': 2
        }
        response = c.post(URL+'/8/report', data=json.dumps(self.post_report_thread_json),
                          content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

        response = c.get(URL+'?'+uri, content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        assert response[Protocol.DATA][0]['id'] != report_thread_id

    def test_get_no_content_from_user2_after_user2_blocked(self):
        get_friend_threads_json = {
            'user': 2,
            'is_friend': True,
            'offset': 0,
            'limit': 1
        }
        post_block_user_json = {
            'user': 2
        }
        post_friend_thread_json = {
            'author': 1,
            'is_public': False,
            'content': 'post_friend_thread_json2'
        }

        c = Client()
        uri = parse.urlencode(get_friend_threads_json)
        response = c.get('/threads?' + uri, content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

        before_content = response[Protocol.DATA][0]['content']
        response = c.post(URL+'/1/block', data=json.dumps(post_block_user_json),
                          content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

        response = c.post('/threads', data=json.dumps(post_friend_thread_json),
                          content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

        response = c.get('/threads?' + uri, content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        assert not response[Protocol.DATA][0]['content'] == 'post_friend_thread_json2'
        assert before_content == response[Protocol.DATA][0]['content']


class ReportedBugTestCase(TestCase):
    fixtures = ['users.json', 'threads.json']

    def setUp(self):
        self.get_friend_threads_json = {
            'user': 2,
            'is_friend': True,
            'offset': 1,
            'limit': 1
        }

    # offset = 10, limit = 10 get no return data. (fixed)
    def test_get_threads(self):
        c = Client()
        uri = parse.urlencode(self.get_friend_threads_json)
        response = c.get(URL+'?'+uri, content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        assert len(response[Protocol.DATA]) != 0
