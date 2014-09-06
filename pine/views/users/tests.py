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
            'password': '123123',
            'device_type': 'android'
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

    # todo 인증번호 요청
    def test_register_auth(self):
        protocol = {
            'username': '01087537711',
        }
        c = Client()
        response = c.post('/users/auth/request',
                          data=json.dumps(protocol),
                          content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

    # todo 인증번호 요청 실패(잘못된 핸드폰 번호)
    def test_register_auth_fail(self):
        protocol = {
            'username': '0108753',
        }
        c = Client()
        response = c.post('/users/auth/request',
                          data=json.dumps(protocol),
                          content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.FAIL

    # todo 아이폰 유저 인증 번호
    def test_register_user_ios(self):
        protocol = {
            'username': '01085174557',
            'password': '01085174557',
            'auth_num': '111111',
            'device_type': 'ios'
        }
        c = Client()
        response = c.post('/users/register',
                          data=json.dumps(protocol),
                          content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

    # todo 아이폰 유저 잘못된 인증 번호
    def test_register_user_ios_fail(self):
        protocol = {
            'username': '01085174557',
            'password': '01085174557',
            'auth_num': '111112',
            'device_type': 'ios'
        }
        c = Client()
        response = c.post('/users/register',
                          data=json.dumps(protocol),
                          content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.FAIL

    # todo 안드로이드 유저 가입 테스트
    def test_register_user_android(self):
        protocol = {
            'username': '01085174557',
            'password': '01085174557',
            'device_type': 'android'
        }
        c = Client()
        response = c.post('/users/register',
                          data=json.dumps(protocol),
                          content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS

class ReportedTestCase(TestCase, LoadFixtures):
    def setUp(self):
        self.client = Client()

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
