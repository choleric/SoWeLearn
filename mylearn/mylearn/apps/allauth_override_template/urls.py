from django.conf.urls import patterns
from django.conf.urls import url
from ...settings import PROJECT_APP_PREFIX


urlpatterns = patterns(PROJECT_APP_PREFIX + '.allauth_override_template.views',
    url(r'^accounts/signup/$', 'signup_learn', name="account_signup_learn"),
    url(r"^password/change/$", 'password_change_learn', name="account_change_password_learn"),
    url(r'^password/reset/$', 'password_reset_learn', name="account_reset_password_learn"),
    url(r'^accounts/login/$', 'signin_learn', name="account_signin_learn"),
)