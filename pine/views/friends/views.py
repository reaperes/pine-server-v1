import json
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

from django.http import HttpResponse
from django.views.decorators.http import require_POST, require_GET

from pine.models import Users, Phones
from pine.pine import Protocol


""" get friends json protocol

request:


response:
    Content-Type: application/json;
    {
        result:     (String, SUCCESS or FAIL),
        message:    (String, error message),
        data:       (Array)
        [
            "01012345678",
            "01023456789",
            ...
        ],
        ...
    }
"""

@login_required
@require_GET
def get_friends_list(request):
    response_data = {
        Protocol.RESULT: Protocol.FAIL,
        Protocol.MESSAGE: ''
    }

    try:
        user_id = int(request.session['user_id'])
        user = Users.objects.get(id=user_id)
        phones = [phone.phone_number for phone in user.friend_phones.all()]
        response_data[Protocol.DATA] = phones
        response_data[Protocol.RESULT] = Protocol.SUCCESS

    except Exception as err:
        response_data[Protocol.MESSAGE] = str(err)

    return HttpResponse(json.dumps(response_data), content_type='application/json')


""" POST get friends

request:
    Content-Type: application/json;
    {
        phone_numbers:  (Array, Friend's phone numbers)
        ["01012345678", ... ]
    }


response:
    Content-Type: application/json;
    {
        result:     (String, SUCCESS or FAIL),
        message:    (String, error message),
        data: [     (Array, phone numbers)
            "01012345678", ...
        ]
    }

    author : hanyong
"""


@login_required
@require_POST
def post_friends_get(request):
    response_data = {
        Protocol.RESULT: Protocol.FAIL,
        Protocol.MESSAGE: ''
    }
    try:
        req_json = json.loads(request.body.decode('utf-8'))
        phone_numbers = req_json['phone_numbers']

        friends = []
        for target_phone_number in phone_numbers:
            query = Phones.objects.filter(phone_number=target_phone_number)
            if query.exists():
                target_phone = query[0]
                if Users.objects.filter(phone=target_phone).exists():
                    friends.append(target_phone_number)

        response_data[Protocol.DATA] = friends
        response_data[Protocol.RESULT] = Protocol.SUCCESS

    except Exception as err:
        response_data[Protocol.MESSAGE] = str(err)

    return HttpResponse(json.dumps(response_data), content_type='application/json')


""" POST create friend to user

request:
    Content-Type: application/json;
    {
        phone_numbers:  (Array, Friend's phone numbers)
        ["01012345678", ... ]
    }


response:
    Content-Type: application/json;
    {
        result:     (String, SUCCESS or FAIL),
        message:    (String, error message),
    }

"""

@login_required
@require_POST
def post_friends_create(request):
    response_data = {
        Protocol.RESULT: Protocol.FAIL,
        Protocol.MESSAGE: ''
    }
    try:
        req_json = json.loads(request.body.decode('utf-8'))
        user_id = int(request.session['user_id'])

        phone_numbers = req_json['phone_numbers']
        user = Users.objects.get(id=user_id)
        from pine.service import friendship
        for target_phone_number in phone_numbers:
            try:
                friendship.create_friendship(user, target_phone_number)
            except IntegrityError as err:
                pass

        response_data[Protocol.RESULT] = Protocol.SUCCESS

    except Exception as err:
        response_data[Protocol.MESSAGE] = str(err)

    return HttpResponse(json.dumps(response_data), content_type='application/json')


""" POST destroy friend to user

request:
    Content-Type: application/json;
    {
        phone_numbers:  (Array, Friend's phone numbers)
        ["01012345678", ... ]
    }


response:
    Content-Type: application/json;
    {
        result:     (String, SUCCESS or FAIL),
        message:    (String, error message),
    }

"""


@login_required
@require_POST
def post_friends_destroy(request):
    response_data = {
        Protocol.RESULT: Protocol.FAIL,
        Protocol.MESSAGE: ''
    }

    try:
        req_json = json.loads(request.body.decode('utf-8'))
        user_id = int(request.session['user_id'])
        user = Users.objects.get(id=user_id)

        phone_numbers = req_json['phone_numbers']
        for target_phone_number in phone_numbers:
            if Phones.objects.filter(phone_number=target_phone_number).exists():
                target_phone = Phones.objects.get(phone_number=target_phone_number)
                user.friend_phones.remove(target_phone)
                target_query = Users.objects.filter(phone=target_phone)
                if not target_query.exists():
                    continue
                target = Users.objects.get(phone=target_phone)

                if user.friends.filter(id=target.id).exists():
                    user.friends.remove(target)
                    target.followings.add(user)

                if user.followings.filter(id=target.id).exists():
                    user.followings.remove(target)

            else:
                response_data[Protocol.MESSAGE] += 'Warn: ' + target_phone_number + " is not in user's phone book list."

        response_data[Protocol.RESULT] = Protocol.SUCCESS

    except Exception as err:
        response_data[Protocol.MESSAGE] = str(err)

    return HttpResponse(json.dumps(response_data), content_type='application/json')


""" GET handshake friend count

request:


response:
    Content-Type: application/json;
    {
        result:     (String, SUCCESS or FAIL),
        message:    (String, error message),
        count:      (Number, handshake friend's count)
    }

"""


@login_required
@require_GET
def get_friends_handshake_count(request):
    response_data = {
        Protocol.RESULT: Protocol.FAIL,
        Protocol.MESSAGE: ''
    }

    try:
        user_id = int(request.session['user_id'])
        user = Users.objects.get(id=user_id)
        response_data['count'] = user.friends.only('id').count()
        response_data[Protocol.RESULT] = Protocol.SUCCESS

    except Exception as err:
        response_data[Protocol.MESSAGE] = str(err)

    return HttpResponse(json.dumps(response_data), content_type='application/json')
