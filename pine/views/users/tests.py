import json

from pine.pine import Protocol
from pine.views.tests_support import process_session, PineTestCase


class UnitTestCase(PineTestCase):
    def test_post_login(self):
        protocol = {
            'username': '01032080403',
            'password': '01032080403'
        }
        response = self.client.post('/users/login',
                                    data=json.dumps(protocol),
                                    content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

    def test_post_no_id_login(self):
        protocol = {
            'username': '0',
            'password': '0'
        }
        response = self.client.post('/users/login',
                                    data=json.dumps(protocol),
                                    content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.FAIL

    def test_post_invalid_password_login(self):
        protocol = {
            'username': '01032080403',
            'password': '0'
        }
        response = self.client.post('/users/login',
                                    data=json.dumps(protocol),
                                    content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.FAIL

    def test_register_user(self):
        protocol = {
            'username': '123123',
            'password': '123123',
            'device_type': 'android'
        }
        response = self.client.post('/users/register',
                                    data=json.dumps(protocol),
                                    content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

    def test_register_invalid_user(self):
        response = self.client.post('/users/register',
                                    data=json.dumps({
                                        'username': '01032080403',
                                        'password': '01032080403'
                                    }),
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

    def test_register_auth(self):
        response = self.client.post('/users/auth/request',
                                    data=json.dumps({
                                        'username': '01087537711',
                                    }),
                                    content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

    def test_register_auth_fail(self):
        response = self.client.post('/users/auth/request',
                                    data=json.dumps({
                                        'username': '0108753',
                                    }),
                                    content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.FAIL

    def test_register_user_ios(self):
        protocol = {
            'username': '01085174557',
            'password': '01085174557',
            'auth_num': '111111',
            'device_type': 'ios'
        }
        response = self.client.post('/users/register',
                                    data=json.dumps(protocol),
                                    content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

    def test_register_user_ios_fail(self):
        protocol = {
            'username': '01085174557',
            'password': '01085174557',
            'auth_num': '111112',
            'device_type': 'ios'
        }
        response = self.client.post('/users/register',
                                    data=json.dumps(protocol),
                                    content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.FAIL

    def test_register_user_android(self):
        protocol = {
            'username': '01085174557',
            'password': '01085174557',
            'device_type': 'android'
        }
        response = self.client.post('/users/register',
                                    data=json.dumps(protocol),
                                    content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS


class ReportedTestCase(PineTestCase):
    def test_register_user_who_already_added_phone_list(self):
        response = self.client.post('/users/register',
                                    data=json.dumps({
                                        'username': '01085174557',
                                        'password': '01085174557',
                                        'device_type': 'android'
                                    }),
                                    content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS
