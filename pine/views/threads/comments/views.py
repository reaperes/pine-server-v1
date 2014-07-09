import json

from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from pine.models import Threads, Users, Comments
from pine.pine import Protocol


@csrf_exempt
def post_and_get_comments(request, thread_id):
    if request.method == 'POST':
        return post_comment(request, thread_id)
    elif request.method == 'GET':
        return get_comments(request, thread_id)


""" get comments json protocol

request uri:

        user:       (Number) Users.id

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
                                        2=thread author's comment,
                                        3=user & thread author's comment),
                comment_user_id:    (Number, User's virtual id),
                likes:              (Number, how many users like),
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
        user_id = int(request.GET.get('user'))
        thread_id = int(thread_id)
        thread = Threads.objects.get(id=thread_id)

        comments = Comments.objects.filter(thread=thread)

        virtual_id_index = 0
        virtual_id = dict()
        for comment in comments:
            comment_type = 0
            if user_id == comment.author_id:
                comment_type |= (1 << 0)
            if comment.author_id == thread.author_id:
                comment_type |= (1 << 1)

            if comment.author_id in virtual_id:
                virtual_id[comment.author_id] += 1
            else:
                virtual_id[comment.author_id] = virtual_id_index
                virtual_id_index += 1

            likes = [user.id for user in comment.likes.only('id')]

            response_data[Protocol.DATA].append({
                'id': comment.id,
                'comment_type': comment_type,
                'comment_user_id': virtual_id[comment.author_id],
                'pub_date': timezone.localtime(comment.pub_date).strftime(r'%Y-%m-%d %H:%M:%S'),
                'likes': len(likes),
                'is_user_like': user_id in likes,
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
        user:       (Number, Users.id),
        content:    (String, 0 < content <= 200)
    }

response:
    Content-Type: application/json;
    {
        result:     (String, SUCCESS('pine') or FAIL('not pine')),
        message:    (String, error message),
    }

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
        user_id = req_json['user']
        user = Users.objects.get(id=user_id)
        content = req_json['content']

        Comments.objects.create(author=user,
                                thread=thread,
                                pub_date=timezone.now(),
                                content=content)

        response_data[Protocol.RESULT] = Protocol.SUCCESS

    except Exception as err:
        response_data[Protocol.MESSAGE] = str(err)

    return HttpResponse(json.dumps(response_data), content_type='application/json')
