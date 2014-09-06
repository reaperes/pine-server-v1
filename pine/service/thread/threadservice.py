from django.utils import timezone

from pine.models import Threads, Users


class ThreadPermissionException(Exception):
    def __init__(self, message, errors):
        Exception.__init__(self, message)
        self.errors = errors


def get_latest_threads(user_id, count=1, offset_id=None, reverse=False):
    if offset_id is not None:
        offset_datetime = Threads.objects.filter(id=offset_id).values('pub_date')[0]['pub_date']

        if reverse is True:
            threads = (Threads.objects
                       .filter(readers__id=user_id, is_public=False, pub_date__gt=offset_datetime)
                       .reverse()[:count])
        else:
            threads = (Threads.objects
                       .filter(readers__id=user_id, is_public=False, pub_date__lt=offset_datetime)[:count])

    else:
        threads = Threads.objects.filter(readers__id=user_id, is_public=False)[0:count]

    ret = []
    for thread in threads:
        thread_type = 1 if user_id == thread.author_id else 0
        likes = [user.id for user in thread.likes.only('id')]
        views = [t.id for t in thread.views.only('id')]

        # if user first read, add view_count on thread
        if user_id != thread.author_id and user_id not in views:
            thread.views.add(Users.objects.get(id=user_id))

        ret.append({
            'id': thread.id,
            'type': thread_type,
            'pub_date': timezone.localtime(thread.pub_date).strftime(r'%Y-%m-%d %H:%M:%S'),
            'like_count': len(likes),
            'view_count': len(views),
            'liked': user_id in likes,
            'image_url': thread.image_url,
            'content': thread.content,
            'comment': len(thread.comments_set.all())
        })
    return ret


def get_thread(user_id, thread_id):
    thread = Threads.objects.get(id=thread_id)
    readers = [user.id for user in thread.readers.only('id')]

    if user_id not in readers:
        raise ThreadPermissionException

    thread_type = 0
    if user_id == thread.author_id:
        thread_type = 1
    likes = [user.id for user in thread.likes.only('id')]
    views = [user.id for user in thread.views.only('id')]

    return {
        'id': thread.id,
        'type': thread_type,
        'pub_date': timezone.localtime(thread.pub_date).strftime(r'%Y-%m-%d %H:%M:%S'),
        'like_count': len(likes),
        'view_count': len(views),
        'liked': user_id in likes,
        'image_url': thread.image_url,
        'content': thread.content,
        'comment': len(thread.comments_set.all())
    }

