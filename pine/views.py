import json
import logging

from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from pine.models import Thread
from pine.pine import Protocol


logger = logging.getLogger(__name__)


class ErrorMessage:
    MALFORMED_JSON_REQUEST = 'Malformed json request'
    MALFORMED_AUTHOR = 'Author parameter is malformed'
    MALFORMED_CONTENT = 'Content parameter is malformed'


@csrf_exempt
def post_thread(request):
    response_data = {
        Protocol.RESULT: Protocol.FAIL,
        Protocol.MESSAGE: ''
    }

    try:
        req_json_str = json.loads(request.body.decode('utf-8'))
        check_request_validation(req_json_str)
        Thread.objects.create(author=req_json_str['author'], content=req_json_str['content'], pub_date=timezone.now())
        response_data = {
            Protocol.RESULT: Protocol.SUCCESS,
            Protocol.MESSAGE: ''
        }

    # if malformed json
    except ValueError:
        response_data[Protocol.MESSAGE] = ErrorMessage.MALFORMED_JSON_REQUEST

    # if malformed protocol
    except AssertionError as err:
        response_data[Protocol.MESSAGE] = str(err)

    return HttpResponse(json.dumps(response_data), content_type='application/json')


def check_request_validation(request_json_str):
    assert 'author' in request_json_str, ErrorMessage.MALFORMED_AUTHOR
    author = request_json_str['author']
    assert author and 0 < len(author) <= 15, ErrorMessage.MALFORMED_AUTHOR

    assert 'content' in request_json_str, ErrorMessage.MALFORMED_CONTENT
    content = request_json_str['content']
    assert content and 0 < len(content) <= 200, ErrorMessage.MALFORMED_CONTENT