import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


"""
    return request symmetric
"""
@csrf_exempt
def pine_test(request):
    if request.method == 'POST':
        req = json.loads(request.body.decode('utf-8'))
        return HttpResponse(json.dumps(req), content_type='application/json')
    elif request.method == 'GET':
        response = {}
        for key in request.GET:
            response[key] = request.GET.get(key)
        return HttpResponse(str(response), content_type='application/json')
