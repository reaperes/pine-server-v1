import os
import json
from threading import Thread
import requests

from django.utils import timezone

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

    ANDROID push

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

    IOS push

    'aps': {
        'alert': (message, String),
        'badge': 1,
    },
    'thread_id': (int),         # PUSH_NEW_THREAD : no need, 나머지 전부 줄것
    'event_date': 'YYYY-mm-dd HH:MM:SS'

"""


def _send_push_message(user_ids, push_type=None, thread_id=None, comment_id=None, summary=None):
    registration_ids = []
    for user_id in user_ids:
        user = Users.objects.get(pk=user_id)
        if user.device == 'android':
            registration_ids.append(user.push_id)
        if user.device == 'ios':
            _send_push_message_ios(user.push_id, push_type=push_type, thread_id=thread_id)

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


def _send_push_message_ios(push_id, push_type=None, thread_id=None):
    if push_id == 'NOALARM':
        return

    message = ''
    if push_type == PUSH_NEW_THREAD:
        message = '당신의 친구가 새로운 글을 남겼습니다'
    elif push_type == PUSH_NEW_COMMENT:
        message = '누군가가 당신의 글에 댓글을 달았습니다'
    elif push_type == PUSH_LIKE_THREAD:
        message = '누군가가 당신의 글에 하트를 달았습니다 ♥'
    elif push_type == PUSH_LIKE_COMMENT:
        message = '누군가 당신의 댓글에 하트를 달았습니다 ♥'

    req = {
        'token': push_id,
        'alert_body': message,
        'event_date': timezone.localtime(timezone.now()).strftime(r'%Y-%m-%d %H:%M:%S')
    }

    if thread_id is not None:
        req['thread_id'] = int(thread_id)

    if push_type == PUSH_NEW_THREAD:
        del req['thread_id']

    response = requests.post('http://125.209.194.90:8000/push/apns', data=json.dumps(req))