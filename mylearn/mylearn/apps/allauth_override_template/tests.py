import json
from models import *
from .forms import SignupFormLearn, SignupFormAdd
from ..projtest import BaseTest
from mylearn.apps.user_profile.models import User

# Create your tests here.
def test_user_quote_form(self):
        quote = UserQuoteForm(data={'aboutUserQuote': 'hello world'})
        print quote
        self.assertEqual(quote.is_valid(), False)

class UserAllAuthTestCase(BaseTest):
    def test_signup_form(self):
        data ={'email': "signup@signup.com",'password1':"signup",'password1':"signup",'password2':"signup",\
            'userFirstName':"ming", 'userLastName':'xing'}
        signup = SignupFormLearn(data)
        print signup.errors
        self.assertEqual(signup.is_valid(), True)

    def test_signup_form_add(self):
        data ={'email': "signup@signup.com",'password1':"signup",'password1':"signup",'password2':"signup",\
            'userFirstName':"ming", 'userLastName':'xing'}
        signup = SignupFormAdd(data)
        print signup.errors
        self.assertEqual(signup.is_valid(), True)

    def test_signup(self):
        data ={'email': "signup@signup.com",'password1':"signup",'password1':"signup",'password2':"signup",\
            'userFirstName':"ming", 'userLastName':'xing'}
        signup = SignupFormLearn(data)
        signup.save()
        user = User.objects.get(email="signup@signup.com")
        self.assertEqual(user.userLastName,"xing")