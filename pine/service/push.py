import os
import json
from threading import Thread
import requests

from pine.models.users import Users

PUSH_NEW_THREAD = 10
PUSH_NEW_COMMENT = 11

PUSH_LIKE_THREAD = 20
PUSH_LIKE_COMMENT = 21


def send_push_message(user_ids, push_type=None, thread_id=None, comment_id=None, summary=None):
    if os.environ['DJANGO_SETTINGS_MODULE'] == 'PineServerProject.settings.local':
        # below code for test
        # _send_push_message(user_ids=user_ids, push_type=push_type, thread_id=thread_id, comment_id=comment_id, summary=summary)
        pass
    else:
        PushThread(user_ids=user_ids, push_type=push_type,
                   thread_id=thread_id, comment_id=comment_id, summary=summary).start()


class PushThread(Thread):
    def __init__(self, user_ids=None, push_type=None, thread_id=None, comment_id=None, summary=None):
        super().__init__()
        self.user_ids = user_ids
        self.push_type = push_type
        self.thread_id = thread_id
        self.comment_id = comment_id
        self.summary = summary

    def run(self):
        _send_push_message(user_ids=self.user_ids, push_type=self.push_type, thread_id=self.thread_id,
                           comment_id=self.comment_id, summary=self.summary)


""" push message protocol

    PUSH_NEW_THREAD = 10
    PUSH_NEW_COMMENT = 11

    PUSH_LIKE_THREAD = 20
    PUSH_LIKE_COMMENT = 21

    {
        'push_type': (int),
        'message': (String),
        'thread_id': (int),
        'comment_id': (int),
        'summary':
    }

"""


def _send_push_message(user_ids, push_type=None, thread_id=None, comment_id=None, summary=None):
    registration_ids = []
    for user_id in user_ids:
        user = Users.objects.get(pk=user_id)
        if user.device == 'android':
            registration_ids.append(user.push_id)

    message = ''
    if push_type == PUSH_NEW_THREAD:
        message = '당신의 친구가 새로운 글을 남겼습니다'
    elif push_type == PUSH_NEW_COMMENT:
        message = '누군가가 당신의 글에 댓글을 달았습니다'
    elif push_type == PUSH_LIKE_THREAD:
        message = '누군가가 당신의 글에 하트를 달았습니다 ♥'
    elif push_type == PUSH_LIKE_COMMENT:
        message = '누군가 당신의 댓글에 하트를 달았습니다 ♥'

    send_data = {
        'push_type': push_type,
        'message': message
    }

    if thread_id is not None:
        send_data['thread_id'] = thread_id
    if comment_id is not None:
        send_data['comment_id'] = comment_id
    if summary is not None:
        send_data['summary'] = summary

    response = requests.post('http://125.209.194.90:8000/push/gcm', data=json.dumps({
        'registration_ids': registration_ids,
        'data': send_data
    }))

    if response.status_code != 200:
        print(response.text)