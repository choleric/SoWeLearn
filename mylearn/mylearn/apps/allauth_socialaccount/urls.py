from django.conf.urls import patterns
from django.conf.urls import url
from ...settings import PROJECT_APP_PREFIX

# all the url will have a /accounts/ as defined in the project urls.py

urlpatterns = patterns(PROJECT_APP_PREFIX + '.allauth_socialaccount.views',
    url(r'^login/error/$', 'login_error_learn', name="socialaccount_login_error_learn"),
<<<<<<< HEAD
    url(r'^login/cancelled/$', 'login_cancelled_learn', name='socialaccount_login_cancelled_learn'),
    url(r'^signup/$', 'signup_learn', name='socialaccount_signup_learn'),
=======
    url(r'^connections/$', 'social_connections', name='socialaccount_connections')
>>>>>>> 03c8a34259266cbdb96743954f493e934816e809
)