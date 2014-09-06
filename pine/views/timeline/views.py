import json
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.views.decorators.http import require_GET

from pine.pine import Protocol
from pine.service.thread import threadservice


""" get friend timeline

request:

    user:           (Number, Users.id),
    count:          (Number, thread count. 0 < x <= 100)

response:
    Content-Type: application/json;
    {
        result:     (String, SUCCESS('pine') or FAIL('not pine')),
        message:    (String, error message),
        data:       (Array)
        [
            {
                id:           (Number, Threads.id),
                type:         (Number, 0-none 1-author),
                like_count:   (Number, how many users like),
                view_count:   (Number, how many users view),
                liked:        (Boolean, if user like or not),
                pub_date:     (String, '%Y-%m-%d %H:%M:%S'),
                image_url:    (String, image url here),
                content:      (String, content <= 200),
                comment:      (Number, how many comments commented)
            },
            {
                ...
            }
        ]
    }

"""


@login_required
@require_GET
def get_latest_friend_timeline(request):
    response_data = {
        Protocol.RESULT: Protocol.FAIL,
        Protocol.MESSAGE: '',
        Protocol.DATA: []
    }

    try:
        user_id = int(request.session['user_id'])
        count = int(request.GET.get('count'))

        threads = threadservice.get_latest_threads(user_id, count=count)

        response_data[Protocol.DATA] = threads
        response_data[Protocol.RESULT] = Protocol.SUCCESS

    except Exception as err:
        response_data[Protocol.MESSAGE] = err

    return HttpResponse(json.dumps(response_data), content_type='application/json')


""" get friend timeline since offset

request:

    offset_id:      (Number, thread id),
    count:          (Number, thread count. 0 < x <= 100)

response:
    Content-Type: application/json;
    {
        result:     (String, SUCCESS('pine') or FAIL('not pine')),
        message:    (String, error message),
        data:       (Array)
        [
            {
                id:           (Number, Threads.id),
                type:         (Number, 0-none 1-author),
                like_count:   (Number, how many users like),
                view_count:   (Number, how many users view),
                liked:        (Boolean, if user like or not),
                pub_date:     (String, '%Y-%m-%d %H:%M:%S'),
                image_url:    (String, image url here),
                content:      (String, content <= 200),
                comment:      (Number, how many comments commented)
            },
            {
                ...
            }
        ]
    }

"""


@login_required
@require_GET
def get_friend_timeline_since_offset(request):
    response_data = {
        Protocol.RESULT: Protocol.FAIL,
        Protocol.MESSAGE: '',
        Protocol.DATA: []
    }

    try:
        user_id = int(request.session['user_id'])
        count = int(request.GET.get('count'))
        offset_id = int(request.GET.get('offset_id'))

        threads = threadservice.get_latest_threads(user_id, count=count, offset_id=offset_id)

        response_data[Protocol.DATA] = threads
        response_data[Protocol.RESULT] = Protocol.SUCCESS

    except Exception as err:
        response_data[Protocol.MESSAGE] = str(err)

    return HttpResponse(json.dumps(response_data), content_type='application/json')


""" get friend timeline previous offset

request:

    offset_id:      (Number, thread id),
    count:          (Number, thread count. 0 < x <= 100)

response:
    Content-Type: application/json;
    {
        result:     (String, SUCCESS('pine') or FAIL('not pine')),
        message:    (String, error message),
        data:       (Array)
        [
            {
                id:           (Number, Threads.id),
                type:         (Number, 0-none 1-author),
                like_count:   (Number, how many users like),
                view_count:   (Number, how many users view),
                liked:        (Boolean, if user like or not),
                pub_date:     (String, '%Y-%m-%d %H:%M:%S'),
                image_url:    (String, image url here),
                content:      (String, content <= 200),
                comment:      (Number, how many comments commented)
            },
            {
                ...
            }
        ]
    }

"""


@login_required
@require_GET
def get_friend_timeline_previous_offset(request):
    response_data = {
        Protocol.RESULT: Protocol.FAIL,
        Protocol.MESSAGE: '',
        Protocol.DATA: []
    }

    try:
        user_id = int(request.session['user_id'])
        count = int(request.GET.get('count'))
        offset_id = int(request.GET.get('offset_id'))

        threads = threadservice.get_latest_threads(user_id, count=count, offset_id=offset_id, reverse=True)

        response_data[Protocol.DATA] = threads
        response_data[Protocol.RESULT] = Protocol.SUCCESS

    except Exception as err:
        response_data[Protocol.MESSAGE] = err

    return HttpResponse(json.dumps(response_data), content_type='application/json')