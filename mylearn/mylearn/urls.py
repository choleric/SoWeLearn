from django.conf.urls import patterns, include, url

import mylearn.user_profile.views

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
)
