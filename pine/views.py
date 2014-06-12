from django.http import HttpResponse
from pine.models import Thread
from django.utils import timezone
import json


# Create your views here.
def post_thread(request):
    request_json = json.loads(request.body.decode('utf-8'))
    Thread.objects.create(author=request_json['author'], content=request_json['content'], pub_date=timezone.now())
    response_data = {'result': 'OK', 'message': ''}
    return HttpResponse(json.dumps(response_data), content_type='application/json')