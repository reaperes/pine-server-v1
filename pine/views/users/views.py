import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.contrib.auth.models import User

from pine.pine import Protocol
from pine.models import Users, Phones


""" post login

request:
    Content-Type: application/json;
    {
        username:       (String),
        password:       (String)
    }


response:
    Content-Type: application/json;
    {
        result:     (String, SUCCESS or FAIL),
        message:    (String, error message)
    }

"""


@csrf_exempt
def post_login(request):
    if request.method == 'GET':
        return HttpResponse(status=400)

    response_data = {
        Protocol.RESULT: Protocol.FAIL,
        Protocol.MESSAGE: ''
    }

    try:
        req_json = json.loads(request.body.decode('utf-8'))
        username = req_json['username']
        password = req_json['password']
        account = auth.authenticate(username=username, password=password)

        if account is not None and account.is_active:
            auth.login(request, account)
            phone = Phones.objects.get(phone_number=username)
            user_id = Users.objects.get(phone=phone)
            request.session['user_id'] = str(user_id)
            response_data[Protocol.RESULT] = Protocol.SUCCESS
        else:
            response_data[Protocol.MESSAGE] = 'Username or password does not match.'

    except Exception as err:
        response_data[Protocol.MESSAGE] = err

    return HttpResponse(json.dumps(response_data), content_type='application/json')


@csrf_exempt
def post_register(request):
    user = User.objects.create_user(username='namhoon', email='namhoon@pine.com', password='helloworld')
    user.save()
    return HttpResponse(status=200)


@csrf_exempt
def post_delete(request):
    user = User.objects.get(username='namhoon')
    user.delete()
    return HttpResponse(status=200)