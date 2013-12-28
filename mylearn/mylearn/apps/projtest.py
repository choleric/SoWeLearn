from django.test import TestCase
from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress

class BaseTest(TestCase):
    pass
  
"""  
test utils
"""
class BaseTestUtil :  
    """  
    util for create user  
        params:  
            user: user model  
    """
    @staticmethod
    def create_user(**kwargs):  
        User = get_user_model()
        user = User.objects.create(**kwargs)

        pwdKey = 'password'
        if pwdKey in kwargs :
            user.set_password('password')
            user.save()

        return user

    @staticmethod
    def create_email(**kwargs) :
        return EmailAddress.objects.create(**kwargs)
