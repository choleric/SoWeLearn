from django.test import TestCase
from mongoengine import connect
from mongoengine.connection import get_db,disconnect
from mongoengine.python_support import PY3
from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress


try:
    from django.conf import settings
except Exception as err:
    if PY3:
        from unittest import TestCase
        # Dummy value so no error
        class settings:
            DBNAME = 'dummy'
    else:
        raise err

#
# WARNING: MUST CLOSE the connection to production database, otherwise all tables will be dropped in _post_teardown function.
#          Because connection is already set up in settings.py
#
disconnect()


class BaseTest(TestCase):
    db_name = 'test_%s' % settings.DBNAME

    def __init__(self, methodName='runtest'):
        super(BaseTest, self).__init__(methodName)
        connect(self.db_name)
        self.db = get_db()

    def _post_teardown(self):
        super(BaseTest, self)._post_teardown()

        for collection in self.db.collection_names():
            if collection == 'system.indexes':
                continue
            self.db.drop_collection(collection)

    def setUp(self):
        if PY3:
            raise SkipTest('django does not have Python 3 support')
          
  
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
        return User.objects.create(**kwargs)

    @staticmethod
    def create_email(**kwargs) :
        return EmailAddress.objects.create(**kwargs)
