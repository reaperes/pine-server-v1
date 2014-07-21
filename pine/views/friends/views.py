import json
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse

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
def get_friends_list(request):
    if request.method == 'POST':
        return HttpResponse(status=400)

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
        response_data[Protocol.MESSAGE] = err

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
def post_friends_create(request):
    if request.method == 'GET':
        return HttpResponse(status=400)

    response_data = {
        Protocol.RESULT: Protocol.FAIL,
        Protocol.MESSAGE: ''
    }

    try:
        req_json = json.loads(request.body.decode('utf-8'))
        user_id = int(request.session['user_id'])

        phone_numbers = req_json['phone_numbers']

        for target_phone_number in phone_numbers:
            user = Users.objects.get(id=user_id)

            target_phone_id = Phones.objects.filter(phone_number=target_phone_number)
            if target_phone_id.exists():
                target_phone = target_phone_id[0]
                target = Users.objects.get(phone=target_phone)
                target_friend_phone_ids = [phone.id for phone in target.friend_phones.only('id')]
                user.friend_phones.add(target_phone)
                user_phone_id = user.phone.id

                flag_target_has_user_phone_id = user_phone_id in target_friend_phone_ids

                if flag_target_has_user_phone_id:
                    user.friends.add(target)    # symmetrical model
                elif flag_target_has_user_phone_id:
                    target.followings.add(user)
                else:
                    user.followings.add(target)

            else:
                friend_phone = Phones.objects.create(phone_number=target_phone_number)
                user.friend_phones.add(friend_phone)

        response_data[Protocol.RESULT] = Protocol.SUCCESS

    except Exception as err:
        response_data[Protocol.MESSAGE] = err

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
def post_friends_destroy(request):
    if request.method == 'GET':
        return HttpResponse(status=400)

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
            target_phone_query = Phones.objects.filter(phone_number=target_phone_number)
            if target_phone_query.exists():
                target_phone = target_phone_query[0]
                target = Users.objects.get(phone=target_phone)

                user.friend_phones.remove(target_phone)

                if user.friends.filter(id=target.id).exists():
                    user.friends.remove(target)
                    target.followings.add(user)

                if user.followings.filter(id=target.id).exists():
                    user.followings.remove(target)

            else:
                response_data[Protocol.MESSAGE] += 'Warn: ' + target_phone_number + " is not in user's phone book list."

        response_data[Protocol.RESULT] = Protocol.SUCCESS

    except Exception as err:
        response_data[Protocol.MESSAGE] = err

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
def get_friends_handshake_count(request):
    if request.method == 'POST':
        return HttpResponse(status=400)

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
        response_data[Protocol.MESSAGE] = err

    return HttpResponse(json.dumps(response_data), content_type='application/json')
