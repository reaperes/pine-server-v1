import json
from urllib import parse

from pine.pine import Protocol
from pine.views.tests_support import PineTestCase, process_session


class IntegrationTestCase(PineTestCase):
    def test_lower_than_4_friends_user_cannot_read_after_other_user_post_thread(self):
        # post thread
        process_session(self.client, user_id=1)
        response = self.client.post('/threads',
                                    data=json.dumps({
                                        'is_public': False,
                                        'content': 'INVALID'
                                    }),
                                    content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS, response

        # check user can get the thread
        process_session(self.client, user_id=4)
        uri = parse.urlencode({
            'count': 1
        })
        response = self.client.get('/timeline/friends?'+uri, content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        assert response[Protocol.DATA][0]['content'] == 'INVALID'

        # check user can not get the thread
        process_session(self.client, user_id=5)
        uri = parse.urlencode({
            'count': 1
        })
        response = self.client.get('/timeline/friends?'+uri, content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        assert response[Protocol.DATA][0]['content'] != 'INVALID'


class ReportedIntegrationTestCase(PineTestCase):
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