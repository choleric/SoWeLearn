import json
import random

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
from django.conf import settings

from allauth.tests import MockedResponse, mocked_response
from allauth.account.models import EmailAddress,EmailConfirmation
from allauth.socialaccount.models import SocialAccount, SocialApp
from allauth.socialaccount import providers
from allauth.socialaccount.providers import registry
from allauth.socialaccount.providers.facebook.provider import FacebookProvider
from allauth.socialaccount.providers.google.provider import GoogleProvider
from allauth.socialaccount.providers.linkedin.provider import LinkedInProvider
from allauth.socialaccount.providers.twitter.provider import TwitterProvider

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

    def _create_user(self,acc ='raymond.penners@gmail.com',pwd = 'password', username = 'user'):
        user = BaseTestUtil.create_user(
                email= acc,
                username = username,
                password = pwd,
                is_active=True
                )

        BaseTestUtil.create_email(
                user=user,
                email=acc,
                primary=True,
                verified=True
                )
        return user

    def _create_user_and_login(self,login = 'raymond.penners@gmail.com', pwd = 'password'):
        user = self._create_user(login, pwd)
        response = self.client.post(reverse('account_login'),
                                    {'login': login,
                                     'password': pwd})
        return user

    def test_login(self):
        resp_mock = self.get_mocked_response()
        if not resp_mock:
            warnings.warn("Cannot test provider %s, no oauth mock"
                          % self.provider.id)
            return
        resp = self.login(resp_mock,)
        self.assertTrue(0<resp['location'].find(settings.LOGIN_REDIRECT_URL),
                        resp['location'])

    def test_login_error_response(self):
        response = self.client.get(reverse('socialaccount_login_error'))
        self.assertEqual(response.status_code, 200)
        #content = json.loads(response.content)
        #self.assertEqual(content["c"], code.SocialAccountLoginFailed, content)

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

    def test_signin_auto_singup(self):
        # When the email was not registered before, as SOCIALACCOUNT_AUTO_SIGNUP=True, the user is automatically
        # signed up.
        email = "raymond.penners@gmail.com"
        self.login(self.get_mocked_response(email = email))
        # Test models
        self._test_for_models_after_signup(uid="630595557", email = email)

    def test_signin_email_already_exist(self):
        acc = "raymond.penners@gmail.com"
        self._create_user()
        response = self.login(self.get_mocked_response(acc))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(0<response['location'].find(reverse('socialaccount_signup_learn')), response)
        #Check that the user exist
        self.assertTrue(User.objects.get(email=acc),"the user does not exist or is not unique")
        #Check the response from social signup page
        signup_response = self.client.get(response['location'])
        self.assertEqual(signup_response.status_code, 200)
        content = json.loads(signup_response.content)
        self.assertEqual(content['c'], code.DuplicateEmailSocialAccount)

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

    def test_username_based_on_provider(self):
        self.login(self.get_mocked_response())
        print 'accout', SocialAccount.objects.all()[0].user.username

    def test_email_unverified(self):
        test_email = 'raymond.penners@gmail.com'
        resp = self.login(self.get_mocked_response(verified_email=False))
        email_address = EmailAddress.objects \
            .get(email=test_email)
        self.assertFalse(email_address.verified)
        if hasattr(settings, 'SOCIALACCOUNT_EMAIL_VERIFICATION') and  settings.SOCIALACCOUNT_EMAIL_VERIFICATION != 'none':
            self.assertTrue(EmailConfirmation.objects
                        .filter(email_address__email=test_email)
                        .exists())
        #self.assertTemplateUsed(resp,
        #                        'account/email/email_confirmation_signup_subject.txt')

    def test_account_connect(self):
        email = 'some@mail.com'
        username = 'user'
        password = '123456'
        user = User.objects.create(username=username,
                                   is_active=True,
                                   email=email)
        user.set_password(password)
        user.save()
        EmailAddress.objects.create(user=user,
                                    email=email,
                                    primary=True,
                                    verified=True)
        #ret = self.client.login(username=email,
        #                  password=password)
        self.client.post(reverse('account_signin_learn'), {
            'login': email,
            'password': password,
            })


        response = self.login(self.get_mocked_response(given_name='user'),
                   process='connect')
        social = SocialAccount.objects.filter(provider = GoogleProvider.id)
        # Check if we connected...
        self.assertTrue(SocialAccount.objects.filter(user=user,
                                                     provider=GoogleProvider.id).exists())
        # For now, we do not pick up any new e-mail addresses on connect
        self.assertEqual(EmailAddress.objects.filter(user=user).count(), 1)
        self.assertEqual(EmailAddress.objects.filter(user=user,
                                                      email=email).count(), 1)

    def test_account_connection_remove_no_password(self):
        self.assertFalse(SocialAccount.objects.filter(
                                                     provider=GoogleProvider.id).exists())
        username = 'sowelearn'
        self.login(self.get_mocked_response(given_name=username),
                   process='login')
        # Check if we connected...
        self.assertTrue(SocialAccount.objects.filter(
                                                     provider=GoogleProvider.id).exists())

        #print self.client.get(reverse('socialaccount_connections'))
        resp = self.client.post(reverse('socialaccount_connections'), {'account':1})
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)
        self.assertEqual(content['c'], code.SocialConnectionFailedNoPassword)

    def test_account_connection_remove(self):
        self.assertFalse(SocialAccount.objects.filter(
                                                     provider=GoogleProvider.id).exists())
        email = 'some@mail.com'
        username = 'user'
        password = '123456'

        self.login(self.get_mocked_response(given_name=username),
                   process='login')

        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()

        self.assertTrue(SocialAccount.objects.filter(
                                                     provider=GoogleProvider.id).exists())

        #print self.client.get(reverse('socialaccount_connections'))
        resp = self.client.post(reverse('socialaccount_connections'), {'account':1})
        self.assertEqual(resp.status_code, 302)
        #remove again
        resp = self.client.post(reverse('socialaccount_connections'), {'account':1})
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)
        self.assertEqual(content['c'], code.SocialConnectionFailed)

    def test_account_connection_remove_not_verified_email(self):
        #if email is not verified, user can't signin.
        pass

class OAuthGenericTestCase(OAuth2GenericTestCase):
    def login(self, resp_mock, process='login'):
        with mocked_response(MockedResponse(200,
                                            'oauth_token=token&'
                                            'oauth_token_secret=psst',
                                            {'content-type':
                                             'text/html'})):
            resp = self.client.get(reverse(self.provider.id + '_login'),
                                   dict(process=process))
        p = urlparse(resp['location'])
        q = parse_qs(p.query)
        complete_url = reverse(self.provider.id+'_callback')
        self.assertGreater(q['oauth_callback'][0]
                           .find(complete_url), 0)
        with mocked_response(MockedResponse(200,
                                            'oauth_token=token&'
                                            'oauth_token_secret=psst',
                                            {'content-type':
                                             'text/html'}),
                             resp_mock):
            resp = self.client.get(complete_url)
        return resp



class LinkedInTests(OAuthGenericTestCase):

    provider = registry.by_id(LinkedInProvider.id)

    def get_mocked_response(self):
        return MockedResponse(200, u"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<person>
  <id>oKmTqN2ffc</id>
  <first-name>R@ymond</first-name>
  <last-name>Penners</last-name>
  <email-address>raymond.penners@intenct.nl</email-address>
  <picture-url>http://m.c.lnkd.licdn.com/mpr/mprx/0_e0hbvSLc8QWo3ggPeVKqvaFR860d342Pogq4vakwx8IJOyR1XJrwRmr5mIx9C0DxWpGMsW9Lb8EQ</picture-url>
  <public-profile-url>http://www.linkedin.com/in/intenct</public-profile-url>
</person>
""")

class TwitterTests(OAuthGenericTestCase):

    provider = registry.by_id(TwitterProvider.id)

    def get_mocked_response(self):
        # FIXME: Replace with actual/complete Twitter response
        return MockedResponse(200, r"""
{"follow_request_sent": false,
 "profile_use_background_image": true,
 "id": 45671919, "verified": false, "profile_text_color": "333333",
 "profile_image_url_https":
       "https://pbs.twimg.com/profile_images/793142149/r_normal.png",
 "profile_sidebar_fill_color": "DDEEF6",
 "is_translator": false, "geo_enabled": false, "entities":
 {"description": {"urls": []}}, "followers_count": 43, "protected": false,
 "location": "The Netherlands", "default_profile_image": false,
 "id_str": "45671919", "status": {"contributors": null, "truncated":
  false, "text": "RT @denibertovic: Okay I'm definitely using django-allauth from now on. So easy to set up, far less time consuming, and it just works. #dja\u2026", "in_reply_to_status_id": null, "id": 400658301702381568, "favorite_count": 0, "source": "<a href=\"http://twitter.com\" rel=\"nofollow\">Twitter Web Client</a>", "retweeted": true, "coordinates": null, "entities": {"symbols": [], "user_mentions": [{"indices": [3, 16], "screen_name": "denibertovic", "id": 23508244, "name": "Deni Bertovic", "id_str": "23508244"}], "hashtags": [{"indices": [135, 139], "text": "dja"}], "urls": []}, "in_reply_to_screen_name": null, "id_str": "400658301702381568", "retweet_count": 6, "in_reply_to_user_id": null, "favorited": false, "retweeted_status": {"lang": "en", "favorited": false, "in_reply_to_user_id": null, "contributors": null, "truncated": false, "text": "Okay I'm definitely using django-allauth from now on. So easy to set up, far less time consuming, and it just works. #django", "created_at": "Sun Jul 28 19:56:26 +0000 2013", "retweeted": true, "in_reply_to_status_id": null, "coordinates": null, "id": 361575897674956800, "entities": {"symbols": [], "user_mentions": [], "hashtags": [{"indices": [117, 124], "text": "django"}], "urls": []}, "in_reply_to_status_id_str": null, "in_reply_to_screen_name": null, "source": "web", "place": null, "retweet_count": 6, "geo": null, "in_reply_to_user_id_str": null, "favorite_count": 8, "id_str": "361575897674956800"}, "geo": null, "in_reply_to_user_id_str": null, "lang": "en", "created_at": "Wed Nov 13 16:15:57 +0000 2013", "in_reply_to_status_id_str": null, "place": null}, "utc_offset": 3600, "statuses_count": 39, "description": "", "friends_count": 83, "profile_link_color": "0084B4", "profile_image_url": "http://pbs.twimg.com/profile_images/793142149/r_normal.png", "notifications": false, "profile_background_image_url_https": "https://abs.twimg.com/images/themes/theme1/bg.png", "profile_background_color": "C0DEED", "profile_background_image_url": "http://abs.twimg.com/images/themes/theme1/bg.png", "name": "Raymond Penners", "lang": "nl", "profile_background_tile": false, "favourites_count": 0, "screen_name": "pennersr", "url": null, "created_at": "Mon Jun 08 21:10:45 +0000 2009", "contributors_enabled": false, "time_zone": "Amsterdam", "profile_sidebar_border_color": "C0DEED", "default_profile": true, "following": false, "listed_count": 1} """)  # noqa

    def test_login(self):
        resp_mock = self.get_mocked_response()
        if not resp_mock:
            warnings.warn("Cannot test provider %s, no oauth mock"
                          % self.provider.id)
            return
        resp = self.login(resp_mock)
        self.assertRedirects(resp, reverse('socialaccount_signup'))
        resp = self.client.get(reverse('socialaccount_signup'))
        sociallogin = resp.context['form'].sociallogin
        data = dict(email="raymond.penners@gmail.com", #This information is added later! twitter does not offer email address
                    username=str(random.randrange(1000, 10000000)),
                    userFirstName= sociallogin.account.user.first_name,
                    userLastName = sociallogin.account.user.last_name)
        resp = self.client.post(reverse('socialaccount_signup'),
                                data=data)
        self.assertEqual('http://testserver/',resp['location'])
        self.assertFalse(resp.context['user'].has_usable_password())
        account = sociallogin.account
        tw_account = account.get_provider_account()
        self.assertEqual(tw_account.get_screen_name(),
                         'pennersr')
        self.assertEqual(tw_account.get_avatar_url(),
                         'http://pbs.twimg.com/profile_images/793142149/r.png')
        self.assertEqual(tw_account.get_profile_url(),
                         'http://twitter.com/pennersr')