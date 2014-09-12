import json
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.http import require_http_methods, require_POST

from pine.models import Threads, Users, Comments
from pine.pine import Protocol
from pine.service.push import send_push_message, PUSH_NEW_COMMENT, PUSH_NEW_COMMENT_FRIEND, PUSH_LIKE_COMMENT


@login_required
@require_http_methods(["GET", "POST"])
def post_and_get_comments(request, thread_id):
    if request.method == 'POST':
        return post_comment(request, thread_id)
    elif request.method == 'GET':
        return get_comments(request, thread_id)


""" get comments json protocol

request:


response:
    Content-Type: application/json;
    {
        result:     (String, SUCCESS('pine') or FAIL('not pine')),
        message:    (String, error message),
        data:       (Array)
        [
            {
                id:                 (Number, Comments.id),
                comment_type:       (Number,
                                        0=normal,
                                        1=user's comment,
                                        2=thread author's comment
                                        3=user & thread author's comment),
                comment_user_id:    (Number, User's virtual id. It starts 1. Thread author is always 0),
                like_count:         (Number, how many users like),
                liked:              (Boolean, if user liked or not),
                pub_date:           (String, '%Y-%m-%d %H:%M:%S'),
                content:            (String, content <= 200)
            }, ...
        ]
    }

"""


def get_comments(request, thread_id):
    response_data = {
        Protocol.RESULT: Protocol.FAIL,
        Protocol.MESSAGE: '',
        Protocol.DATA: []
    }

    try:
        user_id = int(request.session['user_id'])
        thread_id = int(thread_id)
        thread = Threads.objects.get(id=thread_id)

        comments = Comments.objects.filter(thread=thread)

        virtual_id_index = 0
        virtual_id = dict()
        virtual_id[thread.author_id] = virtual_id_index
        virtual_id_index += 1
        for comment in comments:
            comment_type = 0
            if user_id == comment.author_id:
                comment_type |= (1 << 0)
            if comment.author_id == thread.author_id:
                comment_type |= (1 << 1)

            if comment.author_id not in virtual_id:
                virtual_id[comment.author_id] = virtual_id_index
                virtual_id_index += 1

            likes = [user.id for user in comment.likes.only('id')]

            response_data[Protocol.DATA].append({
                'id': comment.id,
                'comment_type': comment_type,
                'comment_user_id': virtual_id[comment.author_id],
                'pub_date': timezone.localtime(comment.pub_date).strftime(r'%Y-%m-%d %H:%M:%S'),
                'like_count': len(likes),
                'liked': user_id in likes,
                'content': comment.content
            })

        response_data[Protocol.RESULT] = Protocol.SUCCESS

    except Exception as err:
        response_data[Protocol.MESSAGE] = str(err)

    return HttpResponse(json.dumps(response_data), content_type='application/json')


""" post comment json protocol

request json:
    Content-Type: application/json;
    {
        content:    (String, 0 < content <= 200)
    }

response:
    Content-Type: application/json;
    {
        result:     (String, SUCCESS('pine') or FAIL('not pine')),
        message:    (String, error message),
    }

    author hanyong
"""


def post_comment(request, thread_id):
    response_data = {
        Protocol.RESULT: Protocol.FAIL,
        Protocol.MESSAGE: '',
    }

    try:
        thread_id = int(thread_id)
        thread = Threads.objects.get(id=thread_id)
        req_json = json.loads(request.body.decode('utf-8'))
        user_id = int(request.session['user_id'])
        user = Users.objects.get(id=user_id)
        content = req_json['content']

        comment = Comments.objects.create(author=user,
                                          thread=thread,
                                          pub_date=timezone.now(),
                                          content=content)

        response_data[Protocol.RESULT] = Protocol.SUCCESS

        if user_id != thread.author_id:
            summary = content[:17]
            if len(content) > 17:
                summary += '...'

            send_push_message([thread.author.pk], push_type=PUSH_NEW_COMMENT, thread_id=thread_id,
                              comment_id=comment.id, summary=summary, image_url=thread.image_url)

        comments = Comments.objects.filter(thread=thread)

        writers = []
        for comment in comments:
            if comment.author_id != user_id and comment.author_id != thread.author_id:
                writers.append(comment.author_id)

        if len(writers) > 0:
            summary = content[:17]
            if len(content) > 17:
                summary += '...'

            send_push_message(set(writers), push_type=PUSH_NEW_COMMENT_FRIEND, thread_id=thread_id,
                              comment_id=comment.id, summary=summary, image_url=thread.image_url)

    except Exception as err:
        response_data[Protocol.MESSAGE] = str(err)

    return HttpResponse(json.dumps(response_data), content_type='application/json')


""" post comment like json protocol

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
def post_comment_like(request, comment_id):
    response_data = {
        Protocol.RESULT: Protocol.FAIL,
        Protocol.MESSAGE: '',
    }

    try:
        user_id = int(request.session['user_id'])
        comment_id = int(comment_id)

        need_to_push = False

        comment = Comments.objects.get(id=comment_id)
        comment_likes = [user.id for user in comment.likes.only('id')]
        if user_id in comment_likes:
            response_data[Protocol.MESSAGE] = 'Warn: User has already liked'
        else:
            comment.likes.add(user_id)
            comment_likes.append(user_id)

        if comment.max_like < len(comment_likes):
            comment.max_like = len(comment_likes)
            need_to_push = True

        comment.save()
        response_data[Protocol.RESULT] = Protocol.SUCCESS

        if need_to_push and user_id != comment.author_id:
            send_push_message([comment.author.pk], push_type=PUSH_LIKE_COMMENT, thread_id=comment.thread_id,
                              comment_id=comment_id, image_url=comment.thread.image_url)

    except Exception as err:
        response_data[Protocol.MESSAGE] = str(err)

    return HttpResponse(json.dumps(response_data), content_type='application/json')


""" post comment unlike json protocol

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
def post_comment_unlike(request, comment_id):
    response_data = {
        Protocol.RESULT: Protocol.FAIL,
        Protocol.MESSAGE: '',
    }

    try:
        user_id = int(request.session['user_id'])
        comment_id = int(comment_id)
        comment = Comments.objects.get(id=comment_id)
        comment_likes = [user.id for user in comment.likes.only('id')]
        if user_id not in comment_likes:
            response_data[Protocol.MESSAGE] = 'Warn: User has never liked'
        else:
            comment.likes.remove(user_id)

        response_data[Protocol.RESULT] = Protocol.SUCCESS

    except Exception as err:
        response_data[Protocol.MESSAGE] = str(err)

    return HttpResponse(json.dumps(response_data), content_type='application/json')


""" post comment report json protocol

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
def post_comment_report(request, comment_id):
    response_data = {
        Protocol.RESULT: Protocol.FAIL,
        Protocol.MESSAGE: ''
    }

    try:
        user_id = int(request.session['user_id'])
        user = Users.objects.get(id=user_id)

        report_comment_id = int(comment_id)
        report_comment = Threads.objects.get(id=report_comment_id)

        if user_id != report_comment.author_id:
            report_comment.reports.add(user)
            response_data[Protocol.RESULT] = Protocol.SUCCESS
        else:
            response_data[Protocol.MESSAGE] = 'Warn: Cannot report yourself'

    except Exception as err:
        response_data[Protocol.MESSAGE] = str(err)

    return HttpResponse(json.dumps(response_data), content_type='application/json')


""" post comment block json protocol

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
def post_comment_block(request, comment_id):
    response_data = {
        Protocol.RESULT: Protocol.FAIL,
        Protocol.MESSAGE: ''
    }

    try:
        comment_id = int(comment_id)
        user_id = int(request.session['user_id'])
        user = Users.objects.get(id=user_id)

        block_comment = Comments.objects.get(id=comment_id)
        block_user = block_comment.author

        if user_id != block_user.pk:
            if block_user not in user.blocks.only('id'):
                user.blocks.add(block_user)
                user.friends.remove(block_user)
                block_user.friends.remove(user)

                response_data[Protocol.RESULT] = Protocol.SUCCESS
        else:
            response_data[Protocol.MESSAGE] = 'Warn: Cannot block yourself'

    except Exception as err:
        response_data[Protocol.MESSAGE] = str(err)

    return HttpResponse(json.dumps(response_data), content_type='application/json')
