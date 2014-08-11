import os
import json
from threading import Thread
import requests

from pine.models.users import Users

PUSH_NEW_THREAD = 0
PUSH_NEW_COMMENT = 1

PUSH_LIKE_THREAD = 10
PUSH_LIKE_COMMENT = 11


def send_push_message(user_ids, message_type=None):
    if os.environ['DJANGO_SETTINGS_MODULE'] == 'PineServerProject.settings.local':
        # below code for test
    # _send_push_message(user_ids=user_ids, message_type=message_type)
        pass
    else:
        PushThread(user_ids=user_ids, message_type=message_type).start()


class PushThread(Thread):
    def __init__(self, user_ids=None, message_type=None):
        super().__init__()
        self.user_ids = user_ids
        self.message_type = message_type

    def run(self):
        _send_push_message(user_ids=self.user_ids, message_type=self.message_type)


def _send_push_message(user_ids, message_type=None):
    registration_ids = []
    for user_id in user_ids:
        user = Users.objects.get(pk=user_id)
        if user.device == 'android':
            registration_ids.append(user.push_id)

    message = 'I want to tell you something.'
    if message_type == PUSH_NEW_THREAD:
        message = '당신의 친구가 새로운 글을 올렸습니다.'
    elif message_type == PUSH_NEW_COMMENT:
        message = '작성하신 글에 새로운 댓글이 달렸습니다.'
    elif message_type == PUSH_LIKE_THREAD:
        message = '작성하신 글에 하트가 달렸습니다 ♥'
    elif message_type == PUSH_LIKE_COMMENT:
        message = '작성하신 댓글에 하트가 달렸습니다 ♥'

    response = requests.post('http://125.209.194.90:8000/push/gcm', data=json.dumps({
        'registration_ids': registration_ids,
        'data': {
            'message': message
        }
    }))

    if response.status_code != 200:
        print(response.text)