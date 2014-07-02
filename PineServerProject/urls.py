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
    url(r'^threads/(?P<thread_id>.*)/like', 'pine.views.threads.views.post_thread_like'),
    url(r'^threads/(?P<thread_id>.*)/unlike', 'pine.views.threads.views.post_thread_unlike'),
    url(r'^threads/(?P<thread_id>.*)/report', 'pine.views.threads.views.post_report_thread'),
    url(r'^users/(?P<block_user_id>.*)/block', 'pine.views.users.views.post_block_user')
)
