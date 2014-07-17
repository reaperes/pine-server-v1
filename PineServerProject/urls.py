from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'PineServerProject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
    url(r'^test.*', 'pine.test.views.pine_test'),
    url(r'^threads$', 'pine.views.threads.views.pine_thread'),
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
    
)
