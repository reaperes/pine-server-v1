import json
from urllib import parse

from django.test import TestCase
from django.test.client import Client

from pine.pine import Protocol


class UnitThreadTestCase(TestCase):
    fixtures = ['users.json', 'threads.json', 'comments.json', 'phones.json']

    def setUp(self):
        self.get_thread_comments_json = {
            'user': 1
        }
        self.post_thread_comment_json = {
            'user': 1,
            'content': 'Hello, world.'
        }
        self.post_comment_like_json = {
            'user': 1
        }
        self.post_comment_unlike_json = {
            'user': 1
        }
        self.post_comment_report_json = {
            'user': 5
        }
        self.post_comment_block_json = {
            'user': 1
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

    def test_post_comment_like(self):
        c = Client()
        response = c.post('/comments/2/like',
                          data=json.dumps(self.post_comment_like_json),
                          content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

    def test_post_comment_unlike(self):
        c = Client()
        response = c.post('/comments/1/unlike',
                          data=json.dumps(self.post_comment_unlike_json),
                          content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        assert response[Protocol.MESSAGE] == ''

    def test_post_comment_report(self):
        c = Client()
        response = c.post('/comments/1/report',
                          data=json.dumps(self.post_comment_report_json),
                          content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        assert response[Protocol.MESSAGE] == ''

    def test_post_comment_block(self):
        c = Client()
        response = c.post('/comments/2/block',
                          data=json.dumps(self.post_comment_report_json),
                          content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        assert response[Protocol.MESSAGE] == ''


class IntegrationThreadTestCase(TestCase):
    fixtures = ['users.json', 'threads.json', 'comments.json', 'phones.json']

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

    def test_get_comment_like_after_post_comment_like(self):
        get_thread_comments_json = {
            'user': 1
        }
        c = Client()
        uri = parse.urlencode(get_thread_comments_json)
        response = json.loads(c.get('/threads/1/comments?'+uri).content.decode('utf-8'))
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        before_comment_like_count = response[Protocol.DATA][0]['likes']

        post_comment_like_json = {
            'user': 4,
        }
        response = c.post('/comments/1/like',
                          data=json.dumps(post_comment_like_json),
                          content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

        get_thread_comments_json = {
            'user': 1
        }
        c = Client()
        uri = parse.urlencode(get_thread_comments_json)
        response = json.loads(c.get('/threads/1/comments?'+uri).content.decode('utf-8'))
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        assert response[Protocol.DATA][0]['likes'] == before_comment_like_count + 1

    def test_get_comment_like_after_post_comment_unlike(self):
        get_thread_comments_json = {
            'user': 1
        }
        c = Client()
        uri = parse.urlencode(get_thread_comments_json)
        response = json.loads(c.get('/threads/1/comments?'+uri).content.decode('utf-8'))
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        before_comment_like_count = response[Protocol.DATA][0]['likes']

        post_comment_unlike_json = {
            'user': 1,
        }
        response = c.post('/comments/1/unlike',
                          data=json.dumps(post_comment_unlike_json),
                          content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

        get_thread_comments_json = {
            'user': 1
        }
        c = Client()
        uri = parse.urlencode(get_thread_comments_json)
        response = json.loads(c.get('/threads/1/comments?'+uri).content.decode('utf-8'))
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        assert response[Protocol.DATA][0]['likes'] == before_comment_like_count - 1
