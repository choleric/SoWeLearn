import json
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.core import mail
from django.conf import settings
from django.contrib.sites.models import Site

from allauth.account.forms import SignupForm

from .forms import SignupFormAdd
from ..projtest import BaseTest
from ..projtest import BaseTestUtil

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
        data ={'email': "signup@signup.com",'password1':"signup",'password2':"signup",\
            'userFirstName':"ming", 'userLastName':'xing'}
        signup = SignupFormAdd(data)
        self.assertEqual(signup.is_valid(), True)

    def test_signup_save(self):
        data ={'email': "signup@signup.com",'password1':"signup",'password2':"signup",\
            'userFirstName':"ming", 'userLastName':'xing'}
        signup = SignupFormAdd(data)
        user = User()
        if signup.is_valid():
            signup.save(user)
        user = User.objects.get(first_name="ming")
        self.assertEqual(user.last_name,"xing",user)

    def test_signup_allauth_form(self):
        data ={'email': "signup@signup.com",'password1':"signup",'password2':"signup",\
            'userFirstName':"ming", 'userLastName':'xing'}
        signup = SignupForm(data)
        self.assertEqual(signup.is_valid(), True, signup.errors)

    def test_signup_allauth_form_email_invalid(self):
        data ={'email': "signup.com",'password1':"signup1",'password2':"signup",\
            'userFirstName':"ming", 'userLastName':'xing'}
        signup = SignupForm(data)
        signupError = dict(signup.errors.items())
        self.assertEqual(signup.is_valid(), False)
        self.assertTrue('email' in signupError)

    def test_signup(self):
        data ={'email': "signup@signup.com",'password1':"signup",'password2':"signup",\
            'userFirstName':"ming", 'userLastName':'xing'}
        resonpse = self.client.post(reverse('account_signup_learn'),data)
        user = User.objects.get(email="signup@signup.com")
        self.assertEqual(user.last_name,"xing",resonpse)

    def test_signup_different_password(self):
        data ={'email': "yoyo@signup.com",'password1':"signup1",'password2':"signup",\
            'userFirstName':"ming", 'userLastName':'xing'}
        response = self.client.post(reverse('account_signup_learn'),data)
        self.assertEqual(response.status_code, 200, response)
        content = json.loads(response.content)
        self.assertEqual(content["c"],3,content)

    def test_signup_email_already_taken(self):
        User.objects.create(email='signup@signup.com',password='pass')
        data2 ={'email': "signup@signup.com",'password1':"signup",'password2':"signup",\
            'userFirstName':"Ming", 'userLastName':'xing'}
        response = self.client.post(reverse('account_signup_learn'),data2)
        self.assertEqual(response.status_code, 200, response)
        content = json.loads(response.content)
        self.assertEqual(content["c"],2,content)

    def test_signup_common_mistakes(self):
        data ={'email': "signup.com",'password1':"2",'password2':"2",\
            'userFirstName':"", 'userLastName':''}
        response = self.client.post(reverse('account_signup_learn'),data)
        self.assertEqual(response.status_code, 200, response)
        content = json.loads(response.content)
        self.assertEqual(content["c"],1,content)

    def test_signipview(self):
        data = {'email': 'test@test.com', 'password': 'test'}
        response = self.client.post(reverse('account_signin_learn'),data)
        self.assertEqual(response.status_code, 200,response)

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
        user = User.objects.get(pk=user.pk)  #Why do we need this?
        self.assertTrue(user.check_password('newpassword'))

    def test_password_change_wrong_oldpassword(self):
        self._create_user_and_login()
        data = {"oldpassword":"wrongpassword", "password1":"newpassword","password2":"newpassword"}
        response = self.client.post(reverse('account_change_password_learn'),data)
        self.assertEqual(response.status_code,200)
        content = json.loads(response.content)
        self.assertEqual(content["c"],5,content)

    def test_password_change_different_password(self):
        self._create_user_and_login()
        data = {"oldpassword":"password", "password1":"newpassword1", "password2":"newpassword2"}
        response = self.client.post(reverse('account_change_password_learn'), data)
        content = json.loads(response.content)
        self.assertEqual(content["c"],3,content)

    def test_password_forgotten_url_protocol(self):
        user = self._create_user()
        resp = self.client.post(reverse('account_reset_password'),{'email': 'create@create.com'})
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['create@create.com'])
        body = mail.outbox[0].body
        self.assertGreater(body.find('http://'), 0)
        url = body[body.find('/password/reset/'):].split()[0]
        current_site = Site.objects.get_current()
        url = '%s://%s%s' %(settings.ACCOUNT_DEFAULT_HTTP_PROTOCOL,
                            "testserver/accounts", url)
        resp = self.client.get(url)
        self.assertTemplateUsed(resp, 'account/password_reset_from_key.html')
        self.client.post(url, {'password1': 'newpass123',
                     'password2': 'newpass123'})
        user = User.objects.get(pk=user.pk)
        self.assertTrue(user.check_password('newpass123'))
        return resp

    def test_password_forgotten_different_password(self):
        data = {"email":"doesNotExist@create.com"}
        response = self.client.post(reverse('account_reset_password_learn'),data)
        self.assertEqual(response.status_code,200,response)
        content = json.loads(response.content)
        self.assertEqual(content["c"],6,content)

    def test_password_forgotten_invalid_email(self):
        data = {"email":"create.com"}
        response = self.client.post(reverse('account_reset_password_learn'), data)
        self.assertEqual(response.status_code,200,response)
        content = json.loads(response.content)
        self.assertEqual(content["c"],7,content)
