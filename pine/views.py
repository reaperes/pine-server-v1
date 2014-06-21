import json
import logging

from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from pine.models import Threads, Users
from pine.pine import Protocol


logger = logging.getLogger(__name__)


class ErrorMessage:
    MALFORMED_JSON_REQUEST = 'Malformed json request'
    MALFORMED_PARAMETER = 'Some parameters are malformed'


@csrf_exempt
def pine_thread(request):
    if request.method == 'POST':
        return post_thread(request)
    elif request.method == 'GET':
        return get_threads(request)


""" post thread json protocol

request json = {
    author:     (Number, Users.pk),
    is_public:  (Boolean)
    content:    (String, content < 200)
}

response json = {
    result:     (Boolean, 'pine' or 'not pine'),
    message:    (String, One of ErrorMessages)
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

        user = Users.objects.get(pk=int(req_json_str['author']))

        thread = Threads.objects.create(author=user,
                                        is_public=bool(req_json_str['is_public']),
                                        pub_date=timezone.now(),
                                        content=req_json_str['content'])
        thread.readers.add(user.id)
        thread.readers.add(*[f for f in user.friends.only('pk')])

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
    try:
        assert 'author' in request_json_str, 'author error'
        author = request_json_str['author']
        assert author, 'author error'

        assert 'is_public' in request_json_str, 'is_public error'
        is_public = bool(request_json_str['is_public'])
        assert is_public is True or is_public is False, 'is_public error'

        assert 'content' in request_json_str, 'content error'
        content = request_json_str['content']
        assert content and 0 < len(content) <= 200, 'content error'
    except AssertionError as err:
        raise AssertionError(err)


""" get thread json protocol

request json = {
    user:       (Number) Users.pk
    is_friend:  (Boolean)
    offset:     (Number) offset, 0 is latest offset    (0 < offset < 10000)
    limit:      (Number) limit                         (0 < limit <= 100)
}

response json = {
    result:     (String, SUCCESS or FAIL)
    message:    (String, One of ErrorMessages)
    data:       (Array, thread data array)
    [
        {
            id:         (Number, pk)
            is_public:  (Boolean)
            content:    (String, content <= 200)
            pub_date:   (String, '%Y-%m-%d %H:%M:%S')
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

        user = int(request.GET.get('user'))
        is_friend = request.GET.get('is_friend')
        offset = int(request.GET.get('offset'))
        limit = int(request.GET.get('limit'))

        if is_friend == 'true' or is_friend == 'True':
            threads = Threads.objects.filter(readers__id=user)[offset:limit]
        else:
            threads = Threads.objects.filter(is_public=True).exclude(readers__id=user)[offset:limit]

        for thread in threads:
            response_data[Protocol.DATA].append({
                'id': thread.id,
                'is_public': thread.is_public,
                'content': thread.content,
                'pub_date': timezone.localtime(thread.pub_date).strftime(r'%Y-%m-%d %H:%M:%S')
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
    try:
        assert request.GET.get('user')
        int(request.GET.get('user'))

        assert request.GET.get('is_friend')
        is_friend = bool(request.GET.get('is_friend'))
        assert is_friend is True or is_friend is False, 'is_friend'

        assert request.GET.get('offset')
        offset = int(request.GET.get('offset'))
        assert isinstance(offset, int) and 0 <= offset < 10000

        assert request.GET.get('limit')
        limit = int(request.GET.get('limit'))
        assert isinstance(limit, int) and 0 < limit <= 100
    except (ValueError, AssertionError) as err:
        raise AssertionError(err)
