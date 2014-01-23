import json
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.core import mail
from django.conf import settings
from django.contrib.sites.models import Site
from django.test import Client
from django.utils.timezone import now

from allauth.account.forms import SignupForm
from allauth.account.models import EmailConfirmation


from .forms import SignupFormAdd
from ..user_profile.models import UserPersonalProfile
from ..projtest import BaseTest
from ..projtest import BaseTestUtil
from mylearn.apps import errcode

User = get_user_model()

# Create your tests here.
class UserAllAuthTestCase(BaseTest):
    def setUp(self):
        if 'allauth.socialaccount' in settings.INSTALLED_APPS:
                    # Otherwise ImproperlyConfigured exceptions may occur
                    from allauth.socialaccount.models import SocialApp
                    sa = SocialApp.objects.create(name='testfb',
                                                  provider='facebook')
                    sa.sites.add(Site.objects.get_current())

    def test_signup_form_add(self):
        data ={'email': "signup@signup.com",'password1':"signup",'password2':"signup",
               'userFirstName':"ming", 'userLastName':'xing'}
        signup = SignupFormAdd(data)
        self.assertEqual(signup.is_valid(), True)

    def test_signup_save(self):
        data ={'email': "signup@signup.com",'password1':"signup",'password2':"signup",
               'userFirstName':"ming", 'userLastName':'xing'}
        signup = SignupFormAdd(data)
        user = User()
        if signup.is_valid():
            signup.save(user)
        user = User.objects.get(first_name="ming")
        self.assertEqual(user.last_name,"xing",user)

    def test_signup_allauth_form(self):
        data ={'email': "signup@signup.com",'password1':"signup",'password2':"signup",
               'userFirstName':"ming", 'userLastName':'xing'}
        signup = SignupForm(data)
        self.assertEqual(signup.is_valid(), True, signup.errors)

    def test_signup_allauth_form_email_invalid(self):
        data ={'email': "signup.com",'password1':"signup1",'password2':"signup",
               'userFirstName':"ming", 'userLastName':'xing'}
        signup = SignupForm(data)
        signupError = dict(signup.errors.items())
        self.assertEqual(signup.is_valid(), False)
        self.assertTrue('email' in signupError)

    def test_signup(self):
        data ={'email': "signup@signup.com",'password1':"signup",'password2':"signup",
               'userFirstName':"ming", 'userLastName':'xing'}
        response = self.client.post(reverse('account_signup_learn'),data)
        self.assertEqual(response.status_code, 302, response)
        user = User.objects.get(email="signup@signup.com")
        self.assertEqual(user.last_name,"xing",response)

    def test_signup_different_password(self):
        data ={'email': "yoyo@signup.com",'password1':"signup1",'password2':"signup",
               'userFirstName':"ming", 'userLastName':'xing'}
        response = self.client.post(reverse('account_signup_learn'),data)
        self.assertEqual(response.status_code, 200, response)
        content = json.loads(response.content)
        self.assertEqual(content["c"], errcode.DifferentPassword, content)

    def test_signup_email_already_taken(self):
        User.objects.create(email='signup@signup.com',password='pass')
        data2 ={'email': "signup@signup.com",'password1':"signup",'password2':"signup",
                'userFirstName':"Ming", 'userLastName':'xing'}
        response = self.client.post(reverse('account_signup_learn'),data2)
        self.assertEqual(response.status_code, 200, response)
        content = json.loads(response.content)
        self.assertEqual(content["c"], errcode.UserExist, content)

    def test_signup_common_mistakes(self):
        data ={'email': "signup.com",'password1':"2",'password2':"2",
            'userFirstName':"", 'userLastName':''}
        response = self.client.post(reverse('account_signup_learn'),data)
        self.assertEqual(response.status_code, 200, response)
        content = json.loads(response.content)
        self.assertEqual(content["c"],errcode.SignupFailure,content)

    def test_email_verification_mandatory(self):
        c = Client()
        # Signup
        self.client.get(reverse('account_signup_learn'))
        resp = c.post(reverse('account_signup_learn'),
                      {'email': 'john@doe.com',
                       'password1': 'johndoe',
                       'password2': 'johndoe',
                       'userFirstName' : 'John',
                       'userLastName':'Doe'})
        # Attempt to login, unverified
        for attempt in [1, 2]:
            resp = c.post(reverse('account_login'),
                          {'login': 'john@doe.com',
                           'password': 'johndoe'},
                          follow=True)
            # is_active is controlled by the admin to manually disable
            # users. I don't want this flag to flip automatically whenever
            # users verify their email adresses.
            self.assertTrue(User.objects.filter(email='john@doe.com',
                                                is_active=True).exists())
            self.assertTemplateUsed(resp,
                                    'account/verification_sent.html')
            # Attempt 1: no mail is sent due to cool-down ,
            # but there was already a mail in the outbox.
            self.assertEqual(len(mail.outbox), attempt)
            self.assertEqual(EmailConfirmation.objects
                             .filter(email_address__email=
                                     'john@doe.com').count(),
                             attempt)
            # Wait for cooldown
            EmailConfirmation.objects.update(sent=now() - timedelta(days=1))
        # Verify, and
        confirmation = EmailConfirmation \
            .objects \
            .filter(email_address__email='john@doe.com')[:1] \
            .get()
        respConfirm = c.get(reverse('account_confirm_email_learn',
                                    args=[confirmation.key]))
        self.assertEqual(respConfirm.status_code, 302)
        self.assertTrue(0<respConfirm['location'].find(reverse('account_signin_learn')), respConfirm['location'])
        # See if profile exists
        userID = User.objects.get(email = 'john@doe.com').pk
        profile = UserPersonalProfile.objects.filter(pk = userID)

        # Re-attempt to login.
        resp = c.post(reverse('account_login'),
                      {'login': 'john@doe.com',
                       'password': 'johndoe'})
        self.assertEqual(resp['location'],'http://testserver'+settings.LOGIN_REDIRECT_URL)

    def test_email_verification_expires(self):
        c = Client()
        # Signup
        response = self.client.get(reverse('account_signup_learn'))
        c.post(reverse('account_signup_learn'),
                      {'email': 'john@doe.com',
                       'password1': 'johndoe',
                       'password2': 'johndoe',
                       'userFirstName' : 'John',
                       'userLastName':'Doe'})
        # Confirmation expires
        EmailConfirmation.objects.update(sent=now() - timedelta(days=4))
        # Verify and get error
        confirmation = EmailConfirmation \
            .objects \
            .filter(email_address__email='john@doe.com')[:1] \
            .get()
        resp = c.get(reverse('account_confirm_email_learn',
                             args=[confirmation.key]))
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)
        self.assertEqual(content["c"],errcode.InvalidConfirmationEmail,content)

    def test_signinview_csrf(self):
        data = {'login': 'test@test.com', 'password': 'test'}
        c = Client(enforce_csrf_checks=True)
        response = c.post(reverse('account_signin_learn'),data)
        self.assertEqual(response.status_code, 403,response)

    def test_signinview(self):
        data = {'login': 'test@test.com', 'password': 'test'}
        response = self.client.post(reverse('account_signin_lea'
                                            'rn'),data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200,response)
        self.assertEqual(content['c'], errcode.SigninFailure, content)

    def test_signipview_empty_email(self):
        data = {'login': '', 'password': 'test'}
        response = self.client.post(reverse('account_signin_learn'),data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200,response)
        self.assertEqual(content['c'], errcode.SigninInvalidField, content)
        self.assertEqual(1, len(content['d']), content)
        self.assertEqual(content['d'][0], errcode.SigninFormField.index('login'), content)

    def test_signipview_empty_password(self):
        data = {'login': 't@t.com', 'password': ''}
        response = self.client.post(reverse('account_signin_learn'),data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200,response)
        self.assertEqual(content['c'], errcode.SigninInvalidField, content)
        self.assertEqual(1, len(content['d']), content)
        self.assertEqual(content['d'][0], errcode.SigninFormField.index('password'), content)

    def test_signipview_invalid_email(self):
        data = {'login': 't', 'password': ''}
        response = self.client.post(reverse('account_signin_learn'),data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200,response)
        self.assertEqual(content['c'], errcode.SigninInvalidField, content)
        self.assertEqual(2, len(content['d']), content)
        self.assertEqual(content['d'][0], errcode.SigninFormField.index('login'), content)
        self.assertEqual(content['d'][1], errcode.SigninFormField.index('password'), content)

    def _create_user(self):
        acc = 'create@create.com'
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
        return user

    def _create_user_and_login(self):
        user = self._create_user()
        response = self.client.post(reverse('account_login'),
                                    {'login': 'create@create.com',
                                     'password': 'password'})
        return user

    def _password_set_or_reset_redirect(self, urlname, usable_password):
        user = self._create_user_and_login()
        if not usable_password:
            user.set_unusable_password()
            user.save()
        resp = self.client.get(reverse(urlname))
        return resp

    def test_password_set_redirect(self):
        resp = self._password_set_or_reset_redirect('account_set_password',True)
        self.assertEqual(resp.status_code, 302)

    def test_password_change(self):
        user = self._create_user_and_login()
        self.assertTrue(user.check_password('password'))
        data = {"oldpassword":"password", "password1":"newpassword","password2":"newpassword"}
        response = self.client.post(reverse('account_change_password_learn'),data)
        self.assertEqual(response.status_code,302)
        user = User.objects.get(pk=user.pk)
        self.assertTrue(user.check_password('newpassword'))

    def test_password_change_wrong_oldpassword(self):
        self._create_user_and_login()
        data = {"oldpassword":"wrongpassword", "password1":"newpassword","password2":"newpassword"}
        response = self.client.post(reverse('account_change_password_learn'),data)
        self.assertEqual(response.status_code,200)
        content = json.loads(response.content)
        self.assertEqual(content["c"],errcode.WrongOldPassword,content)

    def test_password_change_different_password(self):
        self._create_user_and_login()
        data = {"oldpassword":"password", "password1":"newpassword1", "password2":"newpassword2"}
        response = self.client.post(reverse('account_change_password_learn'), data)
        content = json.loads(response.content)
        self.assertEqual(content["c"],errcode.DifferentPassword,content)

    def test_password_forgotten_no_account(self):
        data = {"email":"doesNotExist@create.com"}
        response = self.client.post(reverse('account_reset_password_learn'),data)
        self.assertEqual(response.status_code,200,response)
        content = json.loads(response.content)
        self.assertEqual(content["c"],errcode.EmailNotRegistered,content)

    def test_password_forgotten_invalid_email(self):
        data = {"email":"create.com"}
        response = self.client.post(reverse('account_reset_password_learn'), data)
        self.assertEqual(response.status_code,200,response)
        content = json.loads(response.content)
        self.assertEqual(content["c"],errcode.ResetPasswordFailure,content)


    def test_password_forgotten_url_protocol(self):
        # Send forgot password request
        user = self._create_user()
        resp = self.client.post(reverse('account_reset_password'),{'email': 'create@create.com'})

        #assert email sent to client
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['create@create.com'])
        body = mail.outbox[0].body
        self.assertGreater(body.find('http://'), 0)

        #get the reset password link
        url = body[body.find('/password/reset/'):].split()[0]
        url = '%s://%s%s' %(settings.ACCOUNT_DEFAULT_HTTP_PROTOCOL,
                            "testserver/accounts", url)

        #reset password
        resp = self.client.get(url)
        self.assertTemplateUsed(resp, 'account/password_reset_from_key.html')
        response = self.client.post(url, {'password1': 'newpass123','password2': 'newpass123'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(0<response['location'].find(reverse('account_reset_password_from_key_done')),
                        response['location'])

        #assert reset password result
        user = User.objects.get(pk=user.pk)
        self.assertTrue(user.check_password('newpass123'))

    def test_resetpw_fromkey_wrong_token(self):
        # Send forgot password request
        user = self._create_user()
        resp = self.client.post(reverse('account_reset_password_learn'),{'email': 'create@create.com'})
        # wrong token
        url = "http://testserver/accounts/password/reset/key/1-3np-a7fd45eb77b6656ab641/"
        response = self.client.post(url, {'password1': 'newpass','password2': 'newpass'})
        self.assertEqual(response.status_code,200)
        content = json.loads(response.content)
        self.assertEqual(content["c"],errcode.ResetPasswordFromKeyBadToken)

    def test_resetpw_fromkey_bad_password(self):
        # Send forgot password request
        user = self._create_user()
        resp = self.client.post(reverse('account_reset_password_learn'),{'email': 'create@create.com'})
        #get the reset password link
        body = mail.outbox[0].body
        url = body[body.find('/password/reset/'):].split()[0]
        url = '%s://%s%s' %(settings.ACCOUNT_DEFAULT_HTTP_PROTOCOL,
                            "testserver/accounts", url)
        #Same password
        response = self.client.post(url, {'password1': 'password1','password2': 'password2'})
        self.assertEqual(response.status_code,200)
        content = json.loads(response.content)
        self.assertEqual(content["c"],errcode.DifferentPassword, response)
        #invalid password
        response2 = self.client.post(url, {'password1': 'pass','password2': 'pass'})
        self.assertEqual(response2.status_code,200)
        content2 = json.loads(response2.content)
        self.assertEqual(content2["c"],errcode.ResetpasswordFromKeyCommonFailure, response2)

    def test_signout(self) :
        # create user and login
        user = self._create_user_and_login()
        # sign out
        response = self.client.post(reverse('account_signout_learn'))

        # assert logout response 
        self.assertEqual(302, response.status_code, response.status_code)
        self.assertTrue(0 < response["location"].find(settings.ACCOUNT_LOGOUT_REDIRECT_URL,),
                "%s != %s" % (settings.ACCOUNT_LOGOUT_REDIRECT_URL, response["location"]))

        # check cookie is destroy
        self.assertTrue(
                settings.SESSION_COOKIE_NAME in response.cookies and
                        -1 == response.cookies[settings.SESSION_COOKIE_NAME]["max-age"],
                "cookie not delete: %(cookie)s" %{"cookie": response.cookies})

        # request login_required url
        data = {"oldpassword":"wrongpassword", "password1":"newpassword","password2":"newpassword"}
        response = self.client.post(reverse('account_change_password_learn'),data)

        # assert response 
        self.assertEqual(302, response.status_code, response.status_code)

        self.assertTrue(0 < response["location"].find(settings.LOGIN_URL),
                "location %s, expected %s" %(response["location"], settings.LOGIN_URL))
