import json

from django.test import TestCase
from django.test.client import Client

from pine.pine import Protocol
from pine.views.tests_support import LoadFixtures, process_session


class UnitThreadTestCase(TestCase, LoadFixtures):
    def setUp(self):
        self.client = Client()
        self.post_friends_create_no_pine_user = {
            'phone_numbers': ['01088888878', '01088888788']
        }
        self.post_friends_create_pine_user = {
            'phone_numbers': ['01032080403']
        }
        self.post_friends_create_pine_user2 = {
            'phone_numbers': ['01020863441']
        }
        self.post_friends_destroy_pine_user = {
            'phone_numbers': ['01098590530']
        }
        self.post_friends_destroy_pine_user2 = {
            'phone_numbers': ['01040099179']
        }

    def test_get_friends_list(self):
        process_session(self.client, user_id=2)
        response = self.client.get('/friends/list', content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

    def test_create_no_pine_friend_to_user(self):
        process_session(self.client, user_id=2)
        response = self.client.post('/friends/create',
                                    data=json.dumps(self.post_friends_create_no_pine_user),
                                    content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

    def test_create_pine_friend_to_user_becoming_each_other_friends(self):
        process_session(self.client, user_id=9)
        response = self.client.post('/friends/create',
                                    data=json.dumps(self.post_friends_create_pine_user),
                                    content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

    def test_create_pine_friend_to_user_becoming_user_following(self):
        process_session(self.client, user_id=2)
        response = self.client.post('/friends/create',
                                    data=json.dumps(self.post_friends_create_pine_user2),
                                    content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

    def test_destroy_pine_friend_each_other_friends(self):
        process_session(self.client, user_id=1)
        response = self.client.post('/friends/destroy',
                                    data=json.dumps(self.post_friends_destroy_pine_user),
                                    content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

    def test_destroy_pine_friend_user_following(self):
        process_session(self.client, user_id=2)
        response = self.client.post('/friends/destroy',
                                    data=json.dumps(self.post_friends_destroy_pine_user2),
                                    content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

    def test_get_handshake_friends_count(self):
        process_session(self.client, user_id=1)
        response = self.client.get('/friends/handshake_count', content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS
