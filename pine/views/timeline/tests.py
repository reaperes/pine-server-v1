import json
from urllib import parse

from pine.pine import Protocol
from pine.views.tests_support import PineTestCase, process_session


class UnitThreadTestCase(PineTestCase):
    def test_get_latest_friend_timeline(self):
        process_session(self.client, user_id=1)
        uri = parse.urlencode({
            'count': 2
        })
        response = self.client.get('/timeline/friends?'+uri, content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        assert len(response[Protocol.DATA]) == 2
        assert response[Protocol.DATA][0]['type'] == 1  # thread is not author
        assert response[Protocol.DATA][1]['type'] == 0  # thread is author

    def get_friend_timeline_since_offset(self):
        process_session(self.client, user_id=1)
        uri = parse.urlencode({
            'offset_id': 3,
            'count': 2
        })
        response = self.client.get('/timeline/friends/since_offset?'+uri, content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS, response
        assert len(response[Protocol.DATA]) == 2, response
        assert response[Protocol.DATA][0]['type'] == 0  # thread is not author
        assert response[Protocol.DATA][1]['type'] == 1  # thread is author

    def get_friend_timeline_previous_offset(self):
        process_session(self.client, user_id=1)
        uri = parse.urlencode({
            'offset_id': 5,
            'count': 2
        })
        response = self.client.get('/timeline/friends/previous_offset?'+uri, content_type='application/json').content.decode('utf-8')
        response = json.loads(response)
        assert response[Protocol.RESULT] == Protocol.SUCCESS
        assert len(response[Protocol.DATA]) == 2
        assert response[Protocol.DATA][0]['type'] == 0  # thread is not author
        assert response[Protocol.DATA][1]['type'] == 1  # thread is author
