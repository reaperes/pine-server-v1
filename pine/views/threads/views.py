import re
import json
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.utils import timezone
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.views.decorators.http import require_http_methods, require_GET, require_POST

from pine.models import Threads, Users
from pine.pine import Protocol
from pine.util import fileutil
from pine.service.push import send_push_message, PUSH_NEW_THREAD, PUSH_LIKE_THREAD


""" post thread json protocol

request 1/2:
    Content-Type: multipart/form-data
    ---------- Boundary ----------
    Content-Disposition: form-data; name='json'
    Content-Type: application/json;
    {
        is_public:  (Boolean),
        content:    (String, content < 200)
    }
    ---------- Boundary ----------
    Content-Disposition: form-data; name='bg_image_file'; filename="png_or_jpg_filename_here.jpg"
    Content-Type: image/png
    ... \x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x01 ...

request 2/2:
    Content-Type: application/json;
    {
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

@login_required
@require_http_methods("POST")
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
            user = Users.objects.get(id=int(request.session['user_id']))
            thread = Threads.objects.create(author=user,
                                            is_public=bool(req_json['is_public']),
                                            pub_date=timezone.now(),
                                            image_url=file_name,
                                            content=req_json['content'])

        else:
            req_json = json.loads(request.body.decode('utf-8'))
            image_url = ''

            # insert db
            user = Users.objects.get(id=int(request.session['user_id']))
            thread = Threads.objects.create(author=user,
                                            is_public=bool(req_json['is_public']),
                                            pub_date=timezone.now(),
                                            image_url=image_url,
                                            content=req_json['content'])

        thread.readers.add(user.id)

        readers = []
        for friend in user.friends.only('pk', 'friend_phones'):
            friend_phones = [phone.id for phone in friend.friend_phones.only('pk')]
            if len(friend_phones) >= 4:
                readers.append(friend.pk)

        thread.readers.add(*readers)

        response_data = {
            Protocol.RESULT: Protocol.SUCCESS,
            Protocol.MESSAGE: ''
        }

        summary = req_json['content'][:17]
        if len(req_json['content']) > 17:
            summary += '...'

        send_push_message(readers, push_type=PUSH_NEW_THREAD, thread_id=thread.pk, summary=summary,
                          image_url=thread.image_url)

    # if malformed protocol
    except Exception as err:
        response_data[Protocol.MESSAGE] = str(err)

    return HttpResponse(json.dumps(response_data), content_type='application/json')


""" get thread protocol

request:
    /threads/<thread_id>

    parameter
        thread_id:      (Number, Thread id)


response:
    Content-Type: application/json;
    {
        result:     (String, SUCCESS('pine') or FAIL('not pine')),
        message:    (String, error message),
        data:       (Array)
        {
            id:           (Number, Threads.id),
            type:         (Number, 0-none 1-author),
            like_count:   (Number, how many users like),
            liked:        (Boolean, if user like or not),
            pub_date:     (String, '%Y-%m-%d %H:%M:%S'),
            image_url:    (String, image url here),
            content:      (String, content <= 200),
            comment:      (Number, how many comments commented)
        }
    }

"""


def get_thread(request, thread_id):
    response_data = {
        Protocol.RESULT: Protocol.FAIL,
        Protocol.MESSAGE: '',
    }

    try:
        thread_id = int(thread_id)
        user_id = int(request.session['user_id'])

        thread = Threads.objects.get(id=thread_id)
        readers = [user.id for user in thread.readers.only('id')]

        if user_id in readers:
            thread_type = 0
            if user_id == thread.author_id:
                thread_type = 1
            likes = [user.id for user in thread.likes.only('id')]
            response_data[Protocol.DATA] = {
                'id': thread.id,
                'type': thread_type,
                'pub_date': timezone.localtime(thread.pub_date).strftime(r'%Y-%m-%d %H:%M:%S'),
                'like_count': len(likes),
                'liked': user_id in likes,
                'image_url': thread.image_url,
                'content': thread.content,
                'comment': len(thread.comments_set.all())
            }
            response_data[Protocol.RESULT] = Protocol.SUCCESS
        else:
            response_data[Protocol.MESSAGE] = 'Err: You have no permission on thread.'

    except Exception as err:
        response_data[Protocol.MESSAGE] = str(err)

    return HttpResponse(json.dumps(response_data), content_type='application/json')


""" get thread offset url protocol

request:
    /threads/<thread_id>/offset?is_friend={boolean}

    parameter
        thread_id:      (Number, Thread id)
        is_friend:      (Boolean, friend feed or public feed


response:
    Content-Type: application/json;
    {
        result:     (String, SUCCESS('pine') or FAIL('not pine')),
        message:    (String, error message),
        offset:     (Number, offset number when you request, 0 <= x < 300)
    }

"""


@login_required
@require_GET
def get_thread_offset(request, thread_id):
    response_data = {
        Protocol.RESULT: Protocol.FAIL,
        Protocol.MESSAGE: '',
    }

    try:
        thread_id = int(thread_id)
        user_id = request.session['user_id']
        is_friend = request.GET.get('is_friend')

        if is_friend == 'true' or is_friend == 'True':
            threads = Threads.objects.filter(readers__id=user_id, is_public=False)[0:299]
        else:
            threads = Threads.objects.filter(is_public=True)[0:299]

        idx = 0
        for thread in threads:
            if thread_id == thread.id:
                response_data[Protocol.RESULT] = Protocol.SUCCESS
                response_data['offset'] = idx
                return HttpResponse(json.dumps(response_data), content_type='application/json')
            idx += 1

        response_data[Protocol.MESSAGE] = 'Cannot find thread id in offsets from 0 to 299.'

    except Exception as err:
        response_data[Protocol.MESSAGE] = str(err)

    return HttpResponse(json.dumps(response_data), content_type='application/json')


""" post thread like json protocol

request:


response:
    Content-Type: application/json;
    {
        result:     (String, SUCCESS or FAIL),
        message:    (String, error message)
    }

"""


@login_required
@require_POST
def post_thread_like(request, thread_id):
    response_data = {
        Protocol.RESULT: Protocol.FAIL,
        Protocol.MESSAGE: ''
    }

    try:
        user_id = int(request.session['user_id'])
        user = Users.objects.get(id=user_id)

        need_to_push = False

        # update db
        thread = Threads.objects.get(id=int(thread_id))
        thread_likes = [user.id for user in thread.likes.only('id')]
        if user_id in thread_likes:
            response_data[Protocol.MESSAGE] = 'Warn: User has already liked'
        else:
            thread.likes.add(user)
            thread_likes.append(user.id)

        if thread.max_like < len(thread_likes):
            thread.max_like = len(thread_likes)
            need_to_push = True

        thread.save()
        response_data[Protocol.RESULT] = Protocol.SUCCESS

        if need_to_push and user_id != thread.author_id:
            send_push_message([thread.author.pk], push_type=PUSH_LIKE_THREAD, thread_id=thread_id,
                              image_url=thread.image_url)

    except Exception as err:
        response_data[Protocol.MESSAGE] = str(err)

    return HttpResponse(json.dumps(response_data), content_type='application/json')


""" post thread unlike json protocol

request:


response:
    Content-Type: application/json;
    {
        result:     (String, SUCCESS or FAIL),
        message:    (String, error message)
    }

"""


@login_required
@require_POST
def post_thread_unlike(request, thread_id):
    response_data = {
        Protocol.RESULT: Protocol.FAIL,
        Protocol.MESSAGE: ''
    }

    try:
        user_id = request.session['user_id']
        user = Users.objects.get(id=user_id)

        # update db
        thread = Threads.objects.get(id=int(thread_id))
        thread_likes = [user.id for user in thread.likes.only('id')]
        if user_id in thread_likes:
            thread.likes.remove(user)
        else:
            response_data[Protocol.MESSAGE] = 'Warn: User has never liked'

        response_data[Protocol.RESULT] = Protocol.SUCCESS

    except Exception as err:
        response_data[Protocol.MESSAGE] = str(err)

    return HttpResponse(json.dumps(response_data), content_type='application/json')


""" post report thread json protocol

request:


response:
    Content-Type: application/json;
    {
        result:     (String, SUCCESS or FAIL),
        message:    (String, error message)
    }

"""


@login_required
@require_POST
def post_report_thread(request, thread_id):
    response_data = {
        Protocol.RESULT: Protocol.FAIL,
        Protocol.MESSAGE: ''
    }

    try:
        user_id = int(request.session['user_id'])
        user = Users.objects.get(id=user_id)

        report_thread_id = int(thread_id)
        report_thread = Threads.objects.get(id=report_thread_id)

        if user_id != report_thread.author_id:
            report_thread.reports.add(user)
            report_thread.readers.remove(user)
            response_data[Protocol.RESULT] = Protocol.SUCCESS
        else:
            response_data[Protocol.MESSAGE] = 'Warn: Cannot report yourself.'

    except Exception as err:
        response_data[Protocol.MESSAGE] = str(err)

    return HttpResponse(json.dumps(response_data), content_type='application/json')


""" post block thread(user) protocol

request:


response:
    Content-Type: application/json;
    {
        result:     (String, SUCCESS or FAIL),
        message:    (String, error message)
    }

"""


@login_required
@require_POST
def post_block_thread(request, thread_id):
    response_data = {
        Protocol.RESULT: Protocol.FAIL,
        Protocol.MESSAGE: ''
    }

    try:
        block_thread_id = int(thread_id)
        block_thread = Threads.objects.get(id=block_thread_id)
        block_user = block_thread.author
        user_id = int(request.session['user_id'])
        user = Users.objects.get(id=user_id)

        if user_id != block_user.pk:
            if block_thread.author in user.blocks.only('id'):
                response_data = {
                    Protocol.RESULT: Protocol.SUCCESS,
                    Protocol.MESSAGE: 'Warn: User already blocked.'
                }
            else:
                user.blocks.add(block_user)
                user.friends.remove(block_user)
                block_user.friends.remove(user)

                block_thread.readers.remove(user)

                response_data = {
                    Protocol.RESULT: Protocol.SUCCESS,
                    Protocol.MESSAGE: ''
                }
        else:
            response_data[Protocol.MESSAGE] = 'Warn: Cannot block yourself'

    except Exception as err:
        response_data[Protocol.MESSAGE] = str(err)

    return HttpResponse(json.dumps(response_data), content_type='application/json')
