import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from pine.models.auths import Auths

from pine.pine import Protocol
from pine.models import Users, Phones
from pine.service import send_sms
from pine.util import gen_number


""" post login

request:
    Content-Type: application/json;
    {
        username:       (String),
    }


response:
    Content-Type: application/json;
    {
        result:     (String, SUCCESS or FAIL),
        message:    (String, error message)
    }

"""


@csrf_exempt
@require_POST
def post_auth(request):
    response_data = {
        Protocol.RESULT: Protocol.FAIL,
        Protocol.MESSAGE: ''
    }

    try:
        req_json = json.loads(request.body.decode('utf-8'))
        username = req_json['username']
        auth_num = gen_number.gen_number()
        result_msg = send_sms.send_msg(username, auth_num)

        if result_msg == 'SUCCESS':
            phone = Phones.objects.filter(phone_number=username)

            if phone.exists() is False:
                phone = Phones.objects.create(phone_number=username)
            else:
                phone = phone[0]

            if Auths.objects.filter(phone=phone).exists():
                Auths.objects.filter(phone=phone).update(auth_number=auth_num)
            else:
                Auths.objects.create(phone=phone, auth_number=auth_num)

            response_data[Protocol.RESULT] = Protocol.SUCCESS

    except Exception as err:
        response_data[Protocol.MESSAGE] = str(err)

    return HttpResponse(json.dumps(response_data), content_type='application/json')


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
@require_POST
def post_login(request):
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
            user_id = Users.objects.get(phone=phone).pk
            request.session['user_id'] = str(user_id)
            auth.login(request, account)
            response_data[Protocol.RESULT] = Protocol.SUCCESS
        else:
            response_data[Protocol.MESSAGE] = 'Username or password does not match.'

    except Exception as err:
        response_data[Protocol.MESSAGE] = str(err)

    return HttpResponse(json.dumps(response_data), content_type='application/json')


""" post register

request:
    Content-Type: application/json;
    {
        username:       (String),
        password:       (String),
        auth_num:       (String),
        device_type:    (String, android or ios),

    }

response:
    Content-Type: application/json;
    {
        result:     (String, SUCCESS or FAIL),
        message:    (String, error message)
    }

"""


@csrf_exempt
@require_POST
def post_register(request):
    response_data = {
        Protocol.RESULT: Protocol.FAIL,
        Protocol.MESSAGE: ''
    }

    try:
        req_json = json.loads(request.body.decode('utf-8'))
        username = req_json['username']
        password = req_json['password']
        device_type = req_json['device_type']

        # check auth number
        phone = Phones.objects.filter(phone_number=username)
        if phone.exists() is False:
            if device_type == 'ios':
                raise Exception('ERROR: Should auth first')
            else:
                phone = Phones.objects.create(phone_number=username)
        else:
            phone = phone[0]

        if device_type == 'ios':
            auth_num = req_json['auth_num']
            auths = Auths.objects.get(phone=phone)
            if auth_num != auths.auth_number:
                raise Exception('ERROR: Wrong auth number.')

        # check username is duplicated
        if User.objects.filter(username=username).count():
            raise Exception('ERROR: Duplicated username.')

        account = User.objects.create_user(username=username, password=password)

        Users.objects.create(account=account, phone=phone)
        response_data[Protocol.RESULT] = Protocol.SUCCESS

    except Exception as err:
        response_data[Protocol.MESSAGE] = str(err)

    return HttpResponse(json.dumps(response_data), content_type='application/json')


""" post register push service

request:
    Content-Type: application/json;
    {
        device_type:    (String, android or ios),
        push_id:        (String, registration id)
    }

response:
    Content-Type: application/json;
    {
        result:     (String, SUCCESS or FAIL),
        message:    (String, error message)
    }

"""


@login_required
@require_POST
def post_register_push(request):
    response_data = {
        Protocol.RESULT: Protocol.FAIL,
        Protocol.MESSAGE: ''
    }

    try:
        user_id = int(request.session['user_id'])
        req_json = json.loads(request.body.decode('utf-8'))
        device_type = req_json['device_type'].lower()
        push_id = req_json['push_id']

        user = Users.objects.get(id=user_id)
        if device_type == 'android':
            user.device = 'android'
        elif device_type == 'ios':
            user.device = 'ios'
        user.push_id = push_id
        user.save()
        response_data[Protocol.RESULT] = Protocol.SUCCESS

    except Exception as err:
        response_data[Protocol.MESSAGE] = str(err)

    return HttpResponse(json.dumps(response_data), content_type='application/json')
