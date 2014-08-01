import json
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.http import require_GET

from pine.models import Threads
from pine.pine import Protocol


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
                like_count:   (Number, how many users like),
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
        user_id = request.session['user_id']
        count = int(request.GET.get('count'))

        threads = Threads.objects.filter(readers__id=user_id, is_public=False)[0:count]

        for thread in threads:
            likes = [user.id for user in thread.likes.only('id')]

            response_data[Protocol.DATA].append({
                'id': thread.id,
                'pub_date': timezone.localtime(thread.pub_date).strftime(r'%Y-%m-%d %H:%M:%S'),
                'like_count': len(likes),
                'liked': user_id in likes,
                'image_url': thread.image_url,
                'content': thread.content,
                'comment': len(thread.comments_set.all())
            })

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
                like_count:   (Number, how many users like),
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
        user_id = request.session['user_id']
        count = int(request.GET.get('count'))
        offset_id = int(request.GET.get('offset_id'))

        offset_datetime = Threads.objects.filter(id=offset_id).values('pub_date')[0]['pub_date']

        threads = (Threads.objects
                   .filter(readers__id=user_id, is_public=False, pub_date__gt=offset_datetime)
                   .reverse()[:count])

        for thread in threads:
            likes = [user.id for user in thread.likes.only('id')]

            response_data[Protocol.DATA].append({
                'id': thread.id,
                'pub_date': timezone.localtime(thread.pub_date).strftime(r'%Y-%m-%d %H:%M:%S'),
                'like_count': len(likes),
                'liked': user_id in likes,
                'image_url': thread.image_url,
                'content': thread.content,
                'comment': len(thread.comments_set.all())
            })

        response_data[Protocol.RESULT] = Protocol.SUCCESS

    except Exception as err:
        response_data[Protocol.MESSAGE] = err

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
                like_count:   (Number, how many users like),
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
        user_id = request.session['user_id']
        count = int(request.GET.get('count'))
        offset_id = int(request.GET.get('offset_id'))

        offset_datetime = Threads.objects.filter(id=offset_id).values('pub_date')[0]['pub_date']

        threads = (Threads.objects
                   .filter(readers__id=user_id, is_public=False, pub_date__lt=offset_datetime)[:count])

        for thread in threads:
            likes = [user.id for user in thread.likes.only('id')]

            response_data[Protocol.DATA].append({
                'id': thread.id,
                'pub_date': timezone.localtime(thread.pub_date).strftime(r'%Y-%m-%d %H:%M:%S'),
                'like_count': len(likes),
                'liked': user_id in likes,
                'image_url': thread.image_url,
                'content': thread.content,
                'comment': len(thread.comments_set.all())
            })

        response_data[Protocol.RESULT] = Protocol.SUCCESS

    except Exception as err:
        response_data[Protocol.MESSAGE] = err

    return HttpResponse(json.dumps(response_data), content_type='application/json')