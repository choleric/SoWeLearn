import json
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from ..projtest import BaseTest

# Create your tests here.
class UserAllAuthTestCase2(BaseTest):
    def test_signup(self):
        data ={'email': "signup@signup.com",'password1':"signup",'password2':"signup",\
            'userFirstName':"ming", 'userLastName':'xing'}
        resonpse = self.client.post(reverse('account_signup'),data)
        print resonpse
        User = get_user_model()
        user = User.objects.get(first_name="ming")
        self.assertEqual(user.last_name,"xing")