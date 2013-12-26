from django.conf.urls import patterns
from django.conf.urls import url
from ...settings import PROJECT_APP_PREFIX

# all the url will have a /accounts/ as defined in the project urls.py

urlpatterns = patterns(PROJECT_APP_PREFIX + '.allauth_override_template.views',
    url(r'^signup/$', 'signup_learn', name="account_signup_learn"),
    url(r'^confirm-email/(?P<key>\w+)/$', 'confirm_email_learn', name="account_confirm_email_learn"),
    url(r'^password/change/$', 'password_change_learn', name="account_change_password_learn"),
    url(r'^password/reset/$', 'password_reset_learn', name="account_reset_password_learn"),
    url(r'^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$','password_reset_from_key_learn',
        name="account_reset_password_from_key_learn"),
    url(r'^login/$', 'signin_learn', name="account_signin_learn"),
    url(r'^logout/$', 'signout_learn', name="account_signout_learn"),
)
