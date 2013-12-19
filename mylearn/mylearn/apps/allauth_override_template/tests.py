import json
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test.client import Client
from allauth.account.forms import SignupForm
from .forms import SignupFormAdd
from ..projtest import BaseTest

# Create your tests here.
class UserAllAuthTestCase(BaseTest):
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
        self.assertEqual(user.last_name,"xing")

    def test_signup_email_invalid(self):
        data ={'email': "signup.com",'password1':"signup1",'password2':"signup",\
            'userFirstName':"ming", 'userLastName':'xing'}
        response = self.client.post(reverse('account_signup_learn'),data)
        print response
        self.assertEqual(response.status_code, 200)

    def test_signup_email_already_taken(self):
        User = get_user_model()
        User.objects.create(email='signup',password='pass')
        data2 ={'email': "signup",'password1':"signup",'password2':"signup",\
            'userFirstName':"ming", 'userLastName':'xing'}
        response = self.client.post(reverse('account_signup_learn'),data2)
        print response
        self.assertEqual(response.status_code, 200)