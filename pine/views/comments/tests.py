import json

from django.test import TestCase
from django.test.client import Client

from pine.pine import Protocol
from pine.views.tests_support import LoadFixtures, process_session


class UnitThreadTestCase(TestCase, LoadFixtures):
    def setUp(self):
        self.client = Client()
        self.post_thread_comment_json = {
            'content': 'Hello, world.'
        }

    def test_get_thread_comment(self):
        process_session(self.client, user_id=1)
        response = self.client.get('/threads/1/comments').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        assert response[Protocol.DATA][0]['comment_user_id'] == 0
        assert response[Protocol.DATA][1]['comment_user_id'] == 1
        assert response[Protocol.DATA][0]['like_count'] == 3
        assert response[Protocol.DATA][1]['like_count'] == 0
        assert response[Protocol.DATA][0]['liked'] is True
        assert response[Protocol.DATA][1]['liked'] is False
        assert response[Protocol.DATA][0]['comment_type'] == 3
        assert response[Protocol.DATA][1]['comment_type'] == 0

        process_session(self.client, user_id=4)
        response = self.client.get('/threads/1/comments').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.DATA][0]['comment_type'] == 2
        assert response[Protocol.DATA][2]['comment_type'] == 1
        assert response[Protocol.DATA][2]['comment_user_id'] == 2

    def test_post_thread_comment(self):
        process_session(self.client, user_id=1)
        response = self.client.post('/threads/1/comments',
                                    data=json.dumps(self.post_thread_comment_json),
                                    content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

    def test_post_comment_like(self):
        process_session(self.client, user_id=1)
        response = self.client.post('/comments/2/like',
                                    content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

    def test_post_comment_unlike(self):
        process_session(self.client, user_id=1)
        response = self.client.post('/comments/1/unlike',
                                    content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        assert response[Protocol.MESSAGE] == ''

    def test_post_comment_report(self):
        process_session(self.client, user_id=5)
        response = self.client.post('/comments/1/report',
                                    content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        assert response[Protocol.MESSAGE] == ''

    def test_post_comment_block(self):
        process_session(self.client, user_id=5)
        response = self.client.post('/comments/2/block',
                                    content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        assert response[Protocol.MESSAGE] == ''


class IntegrationThreadTestCase(TestCase, LoadFixtures):
    def test_get_thread_comment_after_post_thread_comment(self):
        process_session(self.client, user_id=1)
        response = json.loads(self.client.get('/threads/2/comments').content.decode('utf-8'))
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        assert len(response[Protocol.DATA]) == 0

        post_thread_comment_json = {
            'content': 'Hello, world.'
        }
        response = self.client.post('/threads/2/comments',
                                    data=json.dumps(post_thread_comment_json),
                                    content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

        response = json.loads(self.client.get('/threads/2/comments').content.decode('utf-8'))
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        assert len(response[Protocol.DATA]) == 1

    def test_get_comment_like_after_post_comment_like(self):
        process_session(self.client, user_id=1)
        response = json.loads(self.client.get('/threads/1/comments').content.decode('utf-8'))
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        before_comment_like_count = response[Protocol.DATA][0]['like_count']

        process_session(self.client, user_id=4)
        response = self.client.post('/comments/1/like',
                                    content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

        process_session(self.client, user_id=1)
        response = json.loads(self.client.get('/threads/1/comments').content.decode('utf-8'))
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        assert response[Protocol.DATA][0]['like_count'] == before_comment_like_count + 1

    def test_get_comment_like_after_post_comment_unlike(self):
        process_session(self.client, user_id=1)
        response = json.loads(self.client.get('/threads/1/comments').content.decode('utf-8'))
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        before_comment_like_count = response[Protocol.DATA][0]['like_count']

        response = self.client.post('/comments/1/unlike',
                                    content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

        response = json.loads(self.client.get('/threads/1/comments').content.decode('utf-8'))
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        assert response[Protocol.DATA][0]['like_count'] == before_comment_like_count - 1


class ReportedTestCase(TestCase, LoadFixtures):
    def setUp(self):
        self.client = Client()

    def test_get_thread_comment_user_id_after_post_thread_comment(self):
        # thread 1 : comment user 1 8 4 1 8
        # Step 1. Setting comments
        process_session(self.client, user_id=1)
        response = self.client.post('/threads/1/comments',
                                    data=json.dumps({'content': 'author comment'}),
                                    content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

        process_session(self.client, user_id=8)
        response = self.client.post('/threads/1/comments',
                                    data=json.dumps({'content': 'user 8 comment'}),
                                    content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

        # Step 2. check comment type 0, 3
        process_session(self.client, user_id=1)
        response = self.client.get('/threads/1/comments').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        assert response[Protocol.DATA][0]['comment_type'] == 3
        assert response[Protocol.DATA][1]['comment_type'] == 0

        # Step 3. check comment type 0, 3
        process_session(self.client, user_id=4)
        response = self.client.get('/threads/1/comments').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        assert response[Protocol.DATA][0]['comment_type'] == 2
        assert response[Protocol.DATA][2]['comment_type'] == 1

        # Step 4. check comment user_id
        assert response[Protocol.DATA][0]['comment_user_id'] == 0
        assert response[Protocol.DATA][1]['comment_user_id'] == 1
        assert response[Protocol.DATA][2]['comment_user_id'] == 2
        assert response[Protocol.DATA][3]['comment_user_id'] == 0
        assert response[Protocol.DATA][4]['comment_user_id'] == 1
