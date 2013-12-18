import json
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from allauth.account.forms import SignupForm
from ..projtest import BaseTest

# Create your tests here.
class UserAllAuthTestCase2(BaseTest):
    def test_signup_allauth_form(self):
        data ={'email': "signup@signup.com",'password1':"signup",'password2':"signup",\
            'userFirstName':"ming", 'userLastName':'xing'}
        signup = SignupForm(data)
        print signup.errors
        self.assertEqual(signup.is_valid(), True)

    def test_signup_allauth_form_email_invalid(self):
        data ={'email': "signup.com",'password1':"signup",'password2':"signup",\
            'userFirstName':"ming", 'userLastName':'xing'}
        signup = SignupForm(data)
        print signup.errors
        self.assertEqual(signup.is_valid(), False)

    def test_signup(self):
        data ={'email': "signup@signup.com",'password1':"signup",'password2':"signup",\
            'userFirstName':"ming", 'userLastName':'xing'}
        resonpse = self.client.post(reverse('account_signup_learn'),data)
        print resonpse
        User = get_user_model()
        user = User.objects.get(email="signup@signup.com")
        self.assertEqual(user.last_name,"xing")

    def test_signup_email_invalid(self):
        data ={'email': "signup.com",'password1':"signup",'password2':"signup",\
            'userFirstName':"ming", 'userLastName':'xing'}
        response = self.client.post(reverse('account_signup_learn'),data)
        print response
        print response.status_code
        self.assertEqual(response.status_code, 200)
