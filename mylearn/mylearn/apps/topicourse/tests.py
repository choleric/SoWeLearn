"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test import TestCase
from mongoengine import connect
from mongoengine.connection import get_db,disconnect
from mongoengine.python_support import PY3
from django.utils.unittest import SkipTest
import bson

# Create your tests here.

from models import *

try:
    from django.test import TestCase
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

class TopicoursesTestCase(TestCase):
    db_name = 'test_%s' % settings.DBNAME


    def __init__(self, methodName='runtest'):

        connect(self.db_name)
        self.db = get_db()
        super(TopicoursesTestCase, self).__init__(methodName)

    def _post_teardown(self):
        super(TopicoursesTestCase, self)._post_teardown()
        for collection in self.db.collection_names():
            if collection == 'system.indexes':
                continue
            self.db.drop_collection(collection)

    def setUp(self):
        if PY3:
            raise SkipTest('django does not have Python 3 support')

    def test_change_topicourses_title(self):
        new_title = 'new topicourses title'
        topicourse = Topicourses.objects.create(topicoursesTitle='test topicourses title', topicoursesCreatorUserID=123)
        self.assertNotEqual(topicourse.topicoursesTitle, new_title)
        topicourse.change_topicourses_title(new_title)
        newtopicourse = Topicourses.objects.get(pk=topicourse.id)
        self.assertEqual(newtopicourse.topicoursesTitle, new_title)

    def test_upload_topiquiz(self):
        topicourse = Topicourses.objects.create(topicoursesTitle='test topicourses title', topicoursesCreatorUserID=123)
        topiquiz = {}
        topiquiz['topiquizQuestion'] = 'quiz question'
        topiquiz['topiquizCreatorUserID'] = 123
        topiquiz['topiquizId'] = bson.objectid.ObjectId()
        topicourse.upload_topiquiz(topiquiz)
        newtopicourse = Topicourses.objects.get(pk=topicourse.id)

        self.assertEqual(newtopicourse.topiquiz[0].topiquizQuestion, topiquiz['topiquizQuestion'])
        self.assertEqual(newtopicourse.topiquiz[0].topiquizCreatorUserID, topiquiz['topiquizCreatorUserID'])

    def test_change_topiquiz(self):
        topicourse = Topicourses.objects.create(topicoursesTitle='test topicourses title', topicoursesCreatorUserID=123)
        topiquiz = {}
        topiquiz['topiquizId'] = bson.objectid.ObjectId()
        topiquiz['topiquizQuestion'] = 'quiz question'
        topiquiz['topiquizCreatorUserID'] = 123
        topicourse.upload_topiquiz(topiquiz)

        newtopicourse = Topicourses.objects.get(pk=topicourse.id)
        newtopiquiz = {}

        #select first quiz to modify, actually we can choose anyone.
        newtopiquiz['topiquizId'] =  newtopicourse.topiquiz[0].topiquizId
        newtopiquiz['topiquizQuestion'] = 'new quiz'
        newtopiquiz['topiquizCreatorUserID'] = 456
        topicourse.update_topiquiz(newtopiquiz)

        newtopicourse = Topicourses.objects.get(pk=topicourse.id)
        self.assertEqual(newtopicourse.topiquiz[0].topiquizQuestion, newtopiquiz['topiquizQuestion'])
        self.assertEqual(newtopicourse.topiquiz[0].topiquizCreatorUserID, newtopiquiz['topiquizCreatorUserID'])

    def test_change_tag(self):
        topicourse = Topicourses.objects.create(topicoursesTitle='test topicourses title', topicoursesCreatorUserID=123, topicourseTag=['testTag1','testTag2'])
        newTag=['testTag1','newTag1','newTag2']
        self.assertNotEqual(topicourse.topicourseTag, newTag)

        topicourse.change_tag(newTag)

        newtopicourse = Topicourses.objects.get(pk=topicourse.id)
        self.assertEqual(newtopicourse.topicourseTag, newTag)