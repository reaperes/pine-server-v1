import json

from django.test import TestCase
from django.test.client import Client


class PineTestCase(TestCase):
    def setUp(self):
        self.client = Client()


def process_session(client, user_id=1):
    # find username
    username = None
    with open('pine/fixtures/auth.json') as data_file:
        auths_json = json.load(data_file)
    for auth in auths_json:
        if auth['pk'] == user_id:
            username = auth['fields']['username']
            break

    # login client
    client.login(username=username, password=username)

    # save user_id to session
    session = client.session
    session['user_id'] = str(user_id)
    session.save()