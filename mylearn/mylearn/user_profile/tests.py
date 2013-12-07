#
# 
#

from django.test import TestCase
#from mongorunner import TestCase
from mongoengine import connect
from mongoengine.connection import get_db,disconnect
from mongoengine.python_support import PY3

# Create your tests here.

import mylearn
from models import *

try:
    from django.test import TestCase
    from django.conf import settings
except Exception as err:
    if PY3:
        from unittest import TestCase
        # Dummy value so no error
        class settings:
            MONGO_DATABASE_NAME = 'dummy'
    else:
        raise err

#
# WARNING: MUST CLOSE the connection to production database, otherwise all tables will be dropped in _post_teardown function.
#          Because connection is already set up in settings.py
#
disconnect()


class UserPersonalProfileTestCase(TestCase):
    db_name = 'test_%s' % settings.DBNAME
    print 'start test UserPersonalProfileTestCase...'

    def __init__(self, methodName='runtest'):

        connect(self.db_name)
        self.db = get_db()
        super(UserPersonalProfileTestCase, self).__init__(methodName)

    def _post_teardown(self):
        super(UserPersonalProfileTestCase, self)._post_teardown()
        for collection in self.db.collection_names():
            if collection == 'system.indexes':
                continue
            self.db.drop_collection(collection)

    def setUp(self):
        if PY3:
            raise SkipTest('django does not have Python 3 support')

    def test_model(self):
        UserPersonalProfile.objects.create(userSkypeID='skypei_id001', aboutUserQuote='my quote', userEmail='007')
        user = UserPersonalProfile.objects.get(userEmail='007')
        self.assertEqual(user.aboutUserQuote, 'my quote')

    def test_change_about_user_quote(self):
        #create test user
        new_quote = 'new quote'
        UserPersonalProfile.objects.create(userSkypeID='skypei_id001', aboutUserQuote='my quote', userEmail='008')

        #test before changing
        user = UserPersonalProfile.objects.get(userEmail='008')
        self.assertNotEqual(user.aboutUserQuote, new_quote)

        user.change_about_user_quote(new_quote)

        #test after changing
        newuser = UserPersonalProfile.objects.get(userEmail='008')
        self.assertEqual(newuser.aboutUserQuote, new_quote)

    def test_change_education_info(self):
        #create test user
        userEducationCredential=[]
        for i in range(0,1):
            educationCredential={}
            educationCredential['userEducationInfo']='test education info'
            educationCredential['IsVerified']=True
            educationCredential['verifiedTimeStamp']=11110
            educationCredential['verifiedStaffId']=11
            userEducationCredential.append(educationCredential)
        UserPersonalProfile.objects.create(userSkypeID='skypei_id001', aboutUserQuote='my quote', userEmail='009',userEducationCredential=userEducationCredential)

        new_userEducationCredential=[]
        for i in range(0,1):
            educationCredential={}
            educationCredential['userEducationInfo']='new education info'
            educationCredential['IsVerified']=True
            educationCredential['verifiedTimeStamp']=11110
            educationCredential['verifiedStaffId']=11
            new_userEducationCredential.append(educationCredential)
        #test before changing
        user = UserPersonalProfile.objects.get(userEmail='009')
        for i in range(0,1):
            self.assertNotEqual(user.userEducationCredential[i].userEducationInfo,new_userEducationCredential[i]['userEducationInfo'])

        user.change_education_info(new_userEducationCredential)
        #test after changing
        newuser = UserPersonalProfile.objects.get(userEmail='009')
        for i in range(0,1):
            self.assertEqual(newuser.userEducationCredential[i].userEducationInfo,new_userEducationCredential[i]['userEducationInfo'])
