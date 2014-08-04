from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'PineServerProject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
    url(r'^test.*', 'pine.test.views.pine_test'),

    url(r'^users/login', 'pine.views.users.views.post_login'),
    url(r'^users/register$', 'pine.views.users.views.post_register'),
    url(r'^users/register/push', 'pine.views.users.views.post_register_push'),

    url(r'^timeline/friends$', 'pine.views.timeline.views.get_latest_friend_timeline'),
    url(r'^timeline/friends/since_offset', 'pine.views.timeline.views.get_friend_timeline_since_offset'),
    url(r'^timeline/friends/previous_offset', 'pine.views.timeline.views.get_friend_timeline_previous_offset'),

    url(r'^threads$', 'pine.views.threads.views.post_thread'),
    url(r'^threads/(?P<thread_id>[0-9]+)$', 'pine.views.threads.views.get_thread'),
    url(r'^threads/(?P<thread_id>[0-9]+)/offset$', 'pine.views.threads.views.get_thread_offset'),
    url(r'^threads/(?P<thread_id>[0-9]+)/like', 'pine.views.threads.views.post_thread_like'),
    url(r'^threads/(?P<thread_id>[0-9]+)/unlike', 'pine.views.threads.views.post_thread_unlike'),
    url(r'^threads/(?P<thread_id>[0-9]+)/report', 'pine.views.threads.views.post_report_thread'),
    url(r'^threads/(?P<thread_id>[0-9]+)/block', 'pine.views.threads.views.post_block_thread'),

    url(r'^threads/(?P<thread_id>[0-9]+)/comments$', 'pine.views.comments.views.post_and_get_comments'),
    url(r'^comments/(?P<comment_id>[0-9]+)/like', 'pine.views.comments.views.post_comment_like'),
    url(r'^comments/(?P<comment_id>[0-9]+)/unlike', 'pine.views.comments.views.post_comment_unlike'),
    url(r'^comments/(?P<comment_id>[0-9]+)/report', 'pine.views.comments.views.post_comment_report'),
    url(r'^comments/(?P<comment_id>[0-9]+)/block', 'pine.views.comments.views.post_comment_block'),

    url(r'^friends/list', 'pine.views.friends.views.get_friends_list'),
    url(r'^friends/create', 'pine.views.friends.views.post_friends_create'),
    url(r'^friends/destroy', 'pine.views.friends.views.post_friends_destroy'),
    url(r'^friends/handshake_count', 'pine.views.friends.views.get_friends_handshake_count')
)
