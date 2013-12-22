import json
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.conf import settings
from django.contrib.sites.models import Site
from allauth.account.forms import SignupForm
from .forms import SignupFormAdd
from ..projtest import BaseTest

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
        User = get_user_model()
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
        User = get_user_model()
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
        User = get_user_model()
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
        print 'status:', response.status_code, '==='
        print response
        #self.assertNotEqual(response.status_code, 200)

    def _create_user_and_login(self):
        User = get_user_model()
        user = User.objects.create(email='create@create.com',
                                   is_active=True)
        user.set_password('password')
        user.save()
        self.client.login(email='create@create.com', password='password')
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

    def test_password_reset(self):
        user = self._create_user_and_login()
        #self.assertEqual(user.password,"password")
        data = {"oldpassword":"password", "password1":"newpassword","password2":"newpassword"}
        response = self.client.post(reverse('account_set_password'),data)
        print response
        self.assertEqual(response.status_code,302)
        self.client.get(reverse('account_logout'))
        response2=self.client.login(email='create@create.com', password='newpassword')
        print response2
        #self.assertEqual(response2.status_code, 200)
