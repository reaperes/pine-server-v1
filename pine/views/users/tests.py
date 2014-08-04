import json

from django.test import TestCase
from django.test.client import Client

from pine.pine import Protocol
from pine.views.tests_support import LoadFixtures, process_session


class UnitTestCase(TestCase, LoadFixtures):
    def setUp(self):
        self.client = Client()

    def test_post_login(self):
        protocol = {
            'username': '01032080403',
            'password': '01032080403'
        }
        c = Client()
        response = c.post('/users/login',
                          data=json.dumps(protocol),
                          content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

    def test_post_no_id_login(self):
        protocol = {
            'username': '0',
            'password': '0'
        }
        c = Client()
        response = c.post('/users/login',
                          data=json.dumps(protocol),
                          content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.FAIL

    def test_post_invalid_password_login(self):
        protocol = {
            'username': '01032080403',
            'password': '0'
        }
        c = Client()
        response = c.post('/users/login',
                          data=json.dumps(protocol),
                          content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.FAIL

    def test_register_user(self):
        protocol = {
            'username': '123123',
            'password': '123123'
        }
        c = Client()
        response = c.post('/users/register',
                          data=json.dumps(protocol),
                          content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

    def test_register_invalid_user(self):
        protocol = {
            'username': '01032080403',
            'password': '01032080403'
        }
        c = Client()
        response = c.post('/users/register',
                          data=json.dumps(protocol),
                          content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.FAIL

    def test_register_push_service(self):
        process_session(self.client, user_id=1)
        response = self.client.post('/users/register/push',
                                    data=json.dumps({
                                        'device_type': 'android',
                                        'push_id': '1234567890'
                                    }), content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS, response
