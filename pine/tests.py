from django.test import TestCase
from pine.models import Thread
from django.utils import timezone
from django.test.client import Client
import json


# Create your tests here.
class ThreadTestCase(TestCase):
    # def setUp(self):
    #     Thread.objects.create(content='Hello?', pub_date=timezone.now())
    #
    # def test_thread_create(self):
    #     thread = Thread.objects.get(content='Hello?')
    #     self.assertEqual(thread.content, 'Hello?')

    def test_post(self):
        c = Client()
        j = {
            'author': '01032080403',
            'content': 'hello, Kang'
        }
        response = c.post('/thread/post', content_type='application/json', data=json.dumps(j))
        print(response.content.decode('utf-8'))