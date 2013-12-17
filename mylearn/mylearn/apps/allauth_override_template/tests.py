import json
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test.client import Client
from .forms import SignupFormAdd
from ..projtest import BaseTest

# Create your tests here.
class UserAllAuthTestCase(BaseTest):
    def test_signup_form_add(self):
        data ={'email': "signup@signup.com",'password1':"signup",'password2':"signup",\
            'userFirstName':"ming", 'userLastName':'xing'}
        signup = SignupFormAdd(data)
        print signup.errors
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
        self.assertEqual(user.last_name,"xing")