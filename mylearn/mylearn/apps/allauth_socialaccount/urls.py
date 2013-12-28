from django.conf.urls import patterns
from django.conf.urls import url
from ...settings import PROJECT_APP_PREFIX

# all the url will have a /accounts/ as defined in the project urls.py

urlpatterns = patterns(PROJECT_APP_PREFIX + '.allauth_override_template.views',
    url(r'^login/error/$', 'login_error_learn', name="socialaccount_login_error_learn"),
)
