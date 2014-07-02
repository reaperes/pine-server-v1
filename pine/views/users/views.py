import re
import json
import logging

from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

from pine.models import Threads, Users
from pine.pine import Protocol
from pine.util import fileutil


""" post block user protocol

request:
    Content-Type: application/json;
    {
        user:       (Number, Users.id)
    }

response:
    Content-Type: application/json;
    {
        result:     (String, SUCCESS or FAIL),
        message:    (String, error message)
    }

"""


@csrf_exempt
def post_block_user(request, block_user_id):
    if request.method == 'GET':
        return HttpResponse(status=400)

    response_data = {
        Protocol.RESULT: Protocol.FAIL,
        Protocol.MESSAGE: ''
    }

    try:
        req_json = json.loads(request.body.decode('utf-8'))
        user_id = int(req_json['user'])

        user = Users.objects.get(id=user_id)
        block_user = Users.objects.get(id=block_user_id)

        if block_user_id in user.blocks.only('id'):
            response_data = {
                Protocol.RESULT: Protocol.SUCCESS,
                Protocol.MESSAGE: 'Warn: User already blocked.'
            }

        else:
            user.blocks.add(block_user)
            block_user.friends.remove(user)

            response_data = {
                Protocol.RESULT: Protocol.SUCCESS,
                Protocol.MESSAGE: ''
            }

    # if malformed json
    except ValueError as err:
        response_data[Protocol.MESSAGE] = str(err)

    # if malformed protocol
    except AssertionError as err:
        response_data[Protocol.MESSAGE] = str(err)

    return HttpResponse(json.dumps(response_data), content_type='application/json')
