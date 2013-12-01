#from django.test import TestCase
from mongorunner import TestCase

# Create your tests here.

from models import *

print 'start test...'

class UserPersonalProfileTestCase(TestCase):
    def setUp(self):
        UserPersonalProfile.objects.create(userSkypeID='skypei_id001', aboutUserQuote='my quote')

    def test_model(self):
        user = UserPersonalProfile.objects(userSkypeID='skype_id001').first()
        print 'user:', user
        self.assertEqual(user.aboutUserQuote, 'my quote')
