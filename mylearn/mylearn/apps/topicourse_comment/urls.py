from django.conf.urls import patterns
from django.conf.urls import url
from django.conf.urls import include
from ...settings import PROJECT_APP_PREFIX

# all the url will have a /accounts/ as defined in the project urls.py

urlpatterns = patterns(PROJECT_APP_PREFIX + '.topicourse_comment.views',
    url(r'^discussion-create/$', 'discussion_create', name="discussion_create"),
    url(r'^comment-create/$', 'comment_create', name="comment_create"),
    url(r'^comment-security/(?P<discussion_id>\d+)/$', 'comment_security', name="comment_security"),
    url(r'', include('django.contrib.comments.urls')),
)
