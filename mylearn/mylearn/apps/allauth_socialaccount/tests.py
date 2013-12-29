import json

from django.test import TestCase
from urlparse import urlparse, parse_qs
import warnings
from django.contrib.sites.models import Site

try:
    from mock import patch
except ImportError:
    from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test.client import RequestFactory
from django.test.utils import override_settings

from allauth.tests import MockedResponse, mocked_response
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount, SocialApp
from allauth.socialaccount import providers
from allauth.socialaccount.providers import registry
from allauth.socialaccount.providers.facebook.provider import FacebookProvider
from allauth.socialaccount.providers.google.provider import GoogleProvider

from ..projtest import BaseTest
from ..projtest import BaseTestUtil
from .. import code

User = get_user_model()

# Create your tests here.


class OAuth2GenericTestCase(TestCase):

    #mock provider to avoid problem><
    class provider(object):
        id = "appid"

    provider = provider()

    def get_mocked_response(self):
        pass

    def get_login_response_json(self, with_refresh_token=True):
        rt = ''
        if with_refresh_token:
            rt = ',"refresh_token": "testrf"'
        return """{
            "uid":"weibo",
            "access_token":"testac"
            %s }""" % rt

    def setUp(self):
        app = SocialApp.objects.create(provider=self.provider.id,
                                       name=self.provider.id,
                                       client_id='app123id',
                                       key=self.provider.id,
                                       secret='dummy')
        app.sites.add(Site.objects.get_current())

    def test_login(self):
        resp_mock = self.get_mocked_response()
        if not resp_mock:
            warnings.warn("Cannot test provider %s, no oauth mock"
                          % self.provider.id)
            return
        resp = self.login(resp_mock,)
        self.assertTrue(0>resp['location'].find(reverse('socialaccount_signup')))

    def test_login_error_response(self):
        response = self.client.get(reverse('socialaccount_login_error'))
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(content["c"], code.SocialAccountLoginFailed, content)

    def test_login_cancelled_response(self):
        response = self.client.get(reverse('socialaccount_login_cancelled_learn'))
        content = json.loads(response.content)
        self.assertEqual(content["c"], code.SocialAccountLoginCancelled, content)

    def login(self, resp_mock, process='login',
              with_refresh_token=True):
        resp = self.client.get(reverse(self.provider.id + '_login'),
                               dict(process=process))
        p = urlparse(resp['location'])
        q = parse_qs(p.query)
        complete_url = reverse(self.provider.id+'_callback')
        self.assertGreater(q['redirect_uri'][0]
                           .find(complete_url), 0)
        response_json = self \
            .get_login_response_json(with_refresh_token=with_refresh_token)
        with mocked_response(
                MockedResponse(
                    200,
                    response_json,
                    {'content-type': 'application/json'}),
                resp_mock):
            resp = self.client.get(complete_url,
                                   {'code': 'test',
                                    'state': q['state'][0]})
        return resp

    def _test_for_models_after_signup(self, uid, email):
        # Social account model
        socialaccount = SocialAccount.objects.get(uid=uid)
        self.assertEqual(socialaccount.user.email, email)
        self.assertEqual(socialaccount.user.username, 'raymond.penners')
        # User model
        user = User.objects.get(id=socialaccount.user_id)
        self.assertEqual(user.email, email, user)
        #Emailaddress model(
        emailAddress = EmailAddress.objects.get(user_id=user.id)
        self.assertEqual(emailAddress.email, email ,emailAddress)
        self.assertEqual(emailAddress.verified, True)

class FacebookTests(OAuth2GenericTestCase):

    provider = registry.by_id(FacebookProvider.id)

    def get_mocked_response(self, email="raymond.penners@gmail.com"):
        return MockedResponse(200, """
        {
           "id": "630595557",
           "name": "Raymond Penners",
           "first_name": "Raymond",
           "last_name": "Penners",
           "email": "%s",
           "link": "https://www.facebook.com/raymond.penners",
           "username": "raymond.penners",
           "birthday": "07/17/1973",
           "work": [
              {
                 "employer": {
                    "id": "204953799537777",
                    "name": "IntenCT"
                 }
              }
           ],
           "timezone": 1,
           "locale": "nl_NL",
           "verified": true,
           "updated_time": "2012-11-30T20:40:33+0000"
        }""" % (email))

    def test_username_auto_singup(self):
        # When the email was not registered before, as SOCIALACCOUNT_AUTO_SIGNUP=True, the user is automatically
        # signed up.
        email = "raymond.penners@gmail.com"
        self.login(self.get_mocked_response(email = email))
        # Test models
        self._test_for_models_after_signup(uid="630595557", email = email)


    def test_signup_failure(self):
        acc = 'raymond.penners@gmail.com'
        pwd = 'password'
        user = BaseTestUtil.create_user(
                email= acc,
                password = pwd,
                is_active=True
                )

        BaseTestUtil.create_email(
                user=user,
                email=acc,
                verified=True
                )
        response = self.login(self.get_mocked_response())
        self.assertEqual(response.status_code, 302)
        self.assertTrue(0>response['location'].find(reverse('socialaccount_signup_learn')), response)

        signup_response = self.post(response['location'], {"email":"%s" %acc})
        self.assertEqual(signup_response.status_code, 302, signup_response)


class GoogleTests(OAuth2GenericTestCase):

    provider = registry.by_id(GoogleProvider.id)

    def get_mocked_response(self,
                            family_name='Penners',
                            given_name='Raymond',
                            name='Raymond Penners',
                            email='raymond.penners@gmail.com',
                            verified_email=True):
        return MockedResponse(200, """
              {"family_name": "%s", "name": "%s",
               "picture": "https://lh5.googleusercontent.com/-GOFYGBVOdBQ/AAAAAAAAAAI/AAAAAAAAAGM/WzRfPkv4xbo/photo.jpg",
               "locale": "nl", "gender": "male",
               "email": "%s",
               "link": "https://plus.google.com/108204268033311374519",
               "given_name": "%s", "id": "108204268033311374519",
               "verified_email": %s }
        """ % (family_name,
               name,
               email,
               given_name,
               (repr(verified_email).lower())))



