import json
from urllib import parse

from django.test import TestCase
from django.test.client import Client

from pine.pine import Protocol
from pine.views.tests_support import LoadFixtures, process_session


class UnitThreadTestCase(TestCase, LoadFixtures):
    def setUp(self):
        self.client = Client()
        self.get_timeline_friend = {
            'count': 2
        }
        self.get_timeline_friend_since_offset = {
            'offset_id': 3,
            'count': 2
        }
        self.get_timeline_friend_previous_offset = {
            'offset_id': 5,
            'count': 2
        }

    def test_get_latest_friend_timeline(self):
        process_session(self.client, user_id=1)
        uri = parse.urlencode(self.get_timeline_friend)
        response = self.client.get('/timeline/friends?'+uri, content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        assert len(response[Protocol.DATA]) == 2

    def get_friend_timeline_since_offset(self):
        process_session(self.client, user_id=1)
        uri = parse.urlencode(self.get_timeline_friend_since_offset)
        response = self.client.get('/timeline/friends/since_offset?'+uri, content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        assert len(response[Protocol.DATA]) == 2

    def get_friend_timeline_previous_offset(self):
        process_session(self.client, user_id=1)
        uri = parse.urlencode(self.get_timeline_friend_previous_offset)
        response = self.client.get('/timeline/friends/previous_offset?'+uri, content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        assert len(response[Protocol.DATA]) == 2
