import json
from urllib import parse

from django.test import TestCase
from django.test.client import Client

from pine.pine import Protocol
from pine.views.tests_support import LoadFixtures, process_session


class IntegrationTestCase(TestCase, LoadFixtures):
    def setUp(self):
        self.client = Client()


class ReportedIntegrationTestCase(TestCase, LoadFixtures):
    def setUp(self):
        self.client = Client()

    def get_thread_data_after_liked(self):
        # User do like
        process_session(self.client, user_id=1)
        response = self.client.post('/threads/5/like',
                                    content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

        # Get timeline thread
        uri = parse.urlencode({
            'count': 20
        })
        response = self.client.get('/timeline/friends?'+uri, content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

        # check data which user liked
        for data in response[Protocol.DATA]:
            if not data['id'] == 5:
                continue
            assert data['liked'] == True, 'liked is false. It should be true.'