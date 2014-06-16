import json
import logging

from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from pine.models import Thread, PineFeed
from pine.pine import Protocol


logger = logging.getLogger(__name__)


class ErrorMessage:
    MALFORMED_JSON_REQUEST = 'Malformed json request'
    POST_MALFORMED_AUTHOR = 'Author parameter is malformed'
    POST_MALFORMED_CONTENT = 'Content parameter is malformed'
    GET_MALFORMED_OFFSET = 'Offset parameter is malformed'
    GET_MALFORMED_LIMIT = 'Limit parameter is malformed'


@csrf_exempt
def pine_thread(request):
    if request.method == 'POST':
        return post_thread(request)
    elif request.method == 'GET':
        return get_threads(request)


""" post thread json protocol

request json = {
    author:     phone number    (limit: <=15),
    content:    content         (limit: <=200)
}

response json = {
    result:     request result                  (SUCCESS or FAIL),
    message:    when result message is fail     (One of ErrorMessages)
}

"""


def post_thread(request):
    response_data = {
        Protocol.RESULT: Protocol.FAIL,
        Protocol.MESSAGE: ''
    }

    try:
        req_json_str = json.loads(request.body.decode('utf-8'))
        check_post_thread_request_validation(req_json_str)
        thread = Thread.objects.create(author=req_json_str['author'], content=req_json_str['content'], pub_date=timezone.now())

        # add pine feed
        PineFeed.objects.create(thread=thread)

        response_data = {
            Protocol.RESULT: Protocol.SUCCESS,
            Protocol.MESSAGE: ''
        }

    # if malformed json
    except ValueError as err:
        print(err)
        response_data[Protocol.MESSAGE] = ErrorMessage.MALFORMED_JSON_REQUEST

    # if malformed protocol
    except AssertionError as err:
        response_data[Protocol.MESSAGE] = str(err)

    return HttpResponse(json.dumps(response_data), content_type='application/json')


def check_post_thread_request_validation(request_json_str):
    assert 'author' in request_json_str, ErrorMessage.POST_MALFORMED_AUTHOR
    author = request_json_str['author']
    assert author and 0 < len(author) <= 15, ErrorMessage.POST_MALFORMED_AUTHOR

    assert 'content' in request_json_str, ErrorMessage.POST_MALFORMED_CONTENT
    content = request_json_str['content']
    assert content and 0 < len(content) <= 200, ErrorMessage.POST_MALFORMED_CONTENT


""" get thread json protocol

request json = {
    offset:     (Number) offset, 0 is latest offset    (0 < offset),
    limit:      (Number) limit                         (0 < limit)
}

response json = {
    result:     (String) request result                  (SUCCESS or FAIL),
    message:    (String) when result message is fail     (One of ErrorMessages),
    data:       (Array)  thread data array
    [
        {
            id,
            pub_date,
            content
        },
        {
            ...
        }
    ]
}

"""


def get_threads(request):
    response_data = {
        Protocol.RESULT: Protocol.FAIL,
        Protocol.MESSAGE: '',
        Protocol.DATA: []
    }

    try:
        check_get_thread_request_validation(request)

        offset = int(request.GET.get('offset'))
        limit = int(request.GET.get('limit'))

        queryset = PineFeed.objects.all()[offset:limit]
        for query in queryset:
            thread = query.thread
            response_data[Protocol.DATA].append({
                'id': thread.id,
                'pub_date': thread.pub_date.strftime(r'%Y-%m-%d %H:%M'),
                'content': thread.content
            })

        response_data[Protocol.RESULT] = Protocol.SUCCESS

    # if malformed json
    except ValueError:
        response_data[Protocol.MESSAGE] = ErrorMessage.MALFORMED_JSON_REQUEST

    # if malformed protocol
    except AssertionError as err:
        response_data[Protocol.MESSAGE] = str(err)

    return HttpResponse(json.dumps(response_data), content_type='application/json')


def check_get_thread_request_validation(request):
    assert request.GET.get('offset'), ErrorMessage.GET_MALFORMED_OFFSET
    offset = request.GET.get('offset')
    try:
        offset = int(offset)
    except ValueError:
        assert False, ErrorMessage.GET_MALFORMED_OFFSET
    assert isinstance(offset, int) and 0 <= offset < 10000, ErrorMessage.GET_MALFORMED_OFFSET

    assert request.GET.get('limit'), ErrorMessage.GET_MALFORMED_LIMIT
    limit = request.GET.get('limit')
    try:
        limit = int(limit)
    except ValueError:
        assert False, ErrorMessage.GET_MALFORMED_LIMIT
    assert isinstance(limit, int) and 0 < limit <= 100, ErrorMessage.GET_MALFORMED_LIMIT
