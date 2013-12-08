from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

import mylearn.user_profile.views
import mylearn.topicourse.views
import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mylearn.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', mylearn.user_profile.views.welcome),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^test/', mylearn.user_profile.views.test),
    url(r'^register/', mylearn.user_profile.views.register_),
    url(r'^login/', mylearn.user_profile.views.login),
    url(r'^profile/', mylearn.user_profile.views.profile),
    url(r'^profile2/', mylearn.user_profile.views.profile2),
    url(r'^userTopicourses/',mylearn.topicourse.views.userTopicourses),
    url(r'^userTopiquestions/',mylearn.topicourse.views.userTopiquestions),
)

urlpatterns += staticfiles_urlpatterns()
