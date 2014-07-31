import json

from django.test import TestCase
from django.test.client import Client

from pine.pine import Protocol
from pine.views.tests_support import LoadFixtures


class UnitTestCase(TestCase, LoadFixtures):
    def setUp(self):
        pass

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
