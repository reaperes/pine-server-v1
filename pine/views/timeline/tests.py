import re
import json
from urllib import parse

from django.test import TestCase
from django.test.client import Client
from django.conf import settings

from pine.pine import Protocol
from pine.views.tests_support import LoadFixtures


class UnitThreadTestCase(TestCase, LoadFixtures):
    def setUp(self):
        self.get_timeline_friend = {
            'user': 1,
            'count': 2
        }
        self.get_timeline_friend_since_offset = {
            'user': 1,
            'offset_id': 3,
            'count': 2
        }
        self.get_timeline_friend_previous_offset = {
            'user': 1,
            'offset_id': 5,
            'count': 2
        }

    def test_get_latest_friend_timeline(self):
        c = Client()
        uri = parse.urlencode(self.get_timeline_friend)
        response = c.get('/timeline/friends?'+uri, content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        assert len(response[Protocol.DATA]) == 2

    def get_friend_timeline_since_offset(self):
        c = Client()
        uri = parse.urlencode(self.get_timeline_friend_since_offset)
        response = c.get('/timeline/friends/since_offset?'+uri, content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        assert len(response[Protocol.DATA]) == 2

    def get_friend_timeline_previous_offset(self):
        c = Client()
        uri = parse.urlencode(self.get_timeline_friend_previous_offset)
        response = c.get('/timeline/friends/previous_offset?'+uri, content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        assert len(response[Protocol.DATA]) == 2
