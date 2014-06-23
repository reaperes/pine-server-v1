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


logger = logging.getLogger(__name__)


class ErrorMessage:
    MALFORMED_JSON_REQUEST = 'Malformed request'
    MALFORMED_PARAMETER = 'Some parameters are malformed'


@csrf_exempt
def pine_thread(request):
    if request.method == 'POST':
        return post_thread(request)
    elif request.method == 'GET':
        return get_threads(request)


""" post thread json protocol

request 1/2:
    Content-Type: multipart/form-data
    ---------- Boundary ----------
    Content-Disposition: form-data; name='json'
    Content-Type: application/json;
    {
        author:     (Number, Users.id),
        is_public:  (Boolean),
        content:    (String, content < 200)
    }
    ---------- Boundary ----------
    Content-Disposition: form-data; name='bg_image_file'; filename="filename_here.png"
    Content-Type: image/png
    ... \x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x01 ...

request 2/2:
    Content-Type: application/json;
    {
        author:     (Number, Users.id),
        is_public:  (Boolean),
        content:    (String, content < 200)
    }


response:
    Content-Type: application/json;
    {
        result:     (String, SUCCESS or FAIL),
        message:    (String, error message)
    }

"""


def post_thread(request):
    response_data = {
        Protocol.RESULT: Protocol.FAIL,
        Protocol.MESSAGE: ''
    }

    try:

        if re.search(r'.*multipart/form-data.*', request.META['CONTENT_TYPE']):
            req_json = json.loads(request.REQUEST['json'])
            req_file = request.FILES['bg_image_file']

            file_name = fileutil.generate_file_name(req_file.name)

            # save file
            default_storage.save(settings.MEDIA_DIR + '/' + file_name, ContentFile(req_file.read()))

            # insert db
            user = Users.objects.get(id=int(req_json['author']))
            thread = Threads.objects.create(author=user,
                                            is_public=bool(req_json['is_public']),
                                            pub_date=timezone.now(),
                                            image_url=file_name,
                                            content=req_json['content'])

        else:
            req_json = json.loads(request.body.decode('utf-8'))
            image_url = ''

            # insert db
            user = Users.objects.get(id=int(req_json['author']))
            thread = Threads.objects.create(author=user,
                                            is_public=bool(req_json['is_public']),
                                            pub_date=timezone.now(),
                                            image_url=image_url,
                                            content=req_json['content'])

        thread.readers.add(user.id)
        thread.readers.add(*[f for f in user.friends.only('pk')])

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


""" get thread json protocol

request:
    Content-Type: application/json;
    {
        user:       (Number) Users.id
        is_friend:  (Boolean)
        offset:     (Number) offset, 0 is latest offset    (0 <= offset < 10000)
        limit:      (Number) limit                         (0 < limit <= 100)
    }

response:
    Content-Type: application/json;
    {
        result:     (String, SUCCESS('pine') or FAIL('not pine')),
        message:    (String, error message),
        data:       (Array)
        [
            {
                id:         (Number, Threads.id),
                pub_date:   (String, '%Y-%m-%d %H:%M:%S'),
                image_url:  (String, image url here),
                content:    (String, content <= 200)
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
        user = int(request.GET.get('user'))
        is_friend = request.GET.get('is_friend')
        offset = int(request.GET.get('offset'))
        limit = int(request.GET.get('limit'))

        if is_friend == 'true' or is_friend == 'True':
            threads = Threads.objects.filter(readers__id=user, is_public=False)[offset:limit]
        else:
            threads = Threads.objects.filter(is_public=True)[offset:limit]

        for thread in threads:
            response_data[Protocol.DATA].append({
                'id': thread.id,
                'is_public': thread.is_public,
                'pub_date': timezone.localtime(thread.pub_date).strftime(r'%Y-%m-%d %H:%M:%S'),
                'image_url': thread.image_url,
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
