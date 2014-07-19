import json
from urllib import parse

from django.test import TestCase
from django.test.client import Client

from pine.pine import Protocol


class UnitThreadTestCase(TestCase):
    fixtures = ['users.json', 'threads.json', 'comments.json', 'phones.json']

    def setUp(self):
        self.get_friends_list = {
            'user': 2
        }
        self.post_friends_create_no_pine_user = {
            'user': 2,
            'phone_numbers': ['01088888878', '01088888788']
        }
        self.post_friends_create_pine_user = {
            'user': 9,
            'phone_numbers': ['01032080403']
        }
        self.post_friends_create_pine_user2 = {
            'user': 2,
            'phone_numbers': ['01020863441']
        }
        self.post_friends_destroy_pine_user = {
            'user': 1,
            'phone_numbers': ['01098590530']
        }
        self.post_friends_destroy_pine_user2 = {
            'user': 2,
            'phone_numbers': ['01040099179']
        }
        self.get_handshake_friend_count = {
            'user': 1
        }

    def test_get_friends_list(self):
        c = Client()
        uri = parse.urlencode(self.get_friends_list)
        response = c.get('/friends/list?'+uri, content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

    def test_create_no_pine_friend_to_user(self):
        c = Client()
        response = c.post('/friends/create',
                          data=json.dumps(self.post_friends_create_no_pine_user),
                          content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

    def test_create_pine_friend_to_user_becoming_each_other_friends(self):
        c = Client()
        response = c.post('/friends/create',
                          data=json.dumps(self.post_friends_create_pine_user),
                          content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

    def test_create_pine_friend_to_user_becoming_user_following(self):
        c = Client()
        response = c.post('/friends/create',
                          data=json.dumps(self.post_friends_create_pine_user2),
                          content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

    def test_destroy_pine_friend_each_other_friends(self):
        c = Client()
        response = c.post('/friends/destroy',
                          data=json.dumps(self.post_friends_destroy_pine_user),
                          content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

    def test_destroy_pine_friend_user_following(self):
        c = Client()
        response = c.post('/friends/destroy',
                          data=json.dumps(self.post_friends_destroy_pine_user2),
                          content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

    def test_get_handshake_friends_count(self):
        c = Client()
        uri = parse.urlencode(self.get_handshake_friend_count)
        response = c.get('/friends/handshake_count?'+uri, content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS
