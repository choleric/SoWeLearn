import json

from django.core.urlresolvers import reverse

from ..projtest import BaseTest
from ..projtest import BaseTestUtil
from mylearn.apps import errcode
from .models import Topicourse

class TopicourseTestCase(BaseTest):
    def _create_user(self):
        acc = 'create@create.com'
        pwd = 'password'
        user = BaseTestUtil.create_user(
                email= acc,
                password = pwd,
                is_active=True
                )


        BaseTestUtil.create_email(
                user=user,
                email=acc,
                verified=True
                )
        return user

    def _create_user_and_login(self):
        user = self._create_user()
        response = self.client.post(reverse('account_login'),
                                    {'login': user.email,
                                     'password': "password"})
        self.assertEquals(302, response.status_code, "login with status: %d" % (response.status_code))
        return user

    def _create_topicourse_at_youtube_callback(self):
        self.__topicourse = Topicourse(
            topicourseVideoID = "videoID",
            topicourseCreatorUserID = self.user.pk,
        )
        self.__topicourse.save()

    def setUp(self) :
        super(TopicourseTestCase, self).setUp()
        self.__user = self._create_user_and_login()
        self._create_topicourse_at_youtube_callback()

    def tearDown(self) :
        self.client.get(reverse('account_signout_learn'))
        self.__user = None

    @property
    def user(self) :
        return self.__user

    @property
    def topicourse(self) :
        return self.__topicourse

    def test_edit_topicourse_info(self):
        topicourseURL = reverse('topicourse')
        params = {
            'topicourseID': self.topicourse.topicourseID,
            'topicourseTitle': "topicourse Title",
            'topicourseContent': "topicourse description",
            'topicourseTag': "tag1, tag2",
            'topicourseType': "type1",
            'topicourseLevel': 0,
        }

        response = self.client.post(topicourseURL, params)
        self.assertEquals(200, response.status_code, "post status errcode %d" %(response.status_code))
        ret = json.loads(response.content)
        self.assertEquals(errcode.SUCCESS, ret["c"], "post errcode %d" %(ret["c"]))

        topicourse = Topicourse.objects.get(topicourseID= self.topicourse.topicourseID)
        self.assertEqual(topicourse.topicourseVideoID, "videoID", topicourse)
        self.assertEqual(topicourse.topicourseTitle, "topicourse Title")
        time = topicourse.topicourseUploadTimeStamp

        params_update = {
            'topicourseID': self.topicourse.topicourseID,
            'topicourseTitle': "topicourse Title updated",
        }
        response = self.client.post(topicourseURL, params_update)
        #Test if the update is complete and the date time field is working properly
        topicourseUpdated = Topicourse.objects.get(topicourseID= self.topicourse.topicourseID)
        self.assertEqual(topicourseUpdated.topicourseVideoID, "videoID", topicourseUpdated)
        self.assertEqual(topicourseUpdated.topicourseTitle, "topicourse Title updated")
        self.assertEqual(topicourseUpdated.topicourseUploadTimeStamp, time)


    def test_edit_topicourse_error(self):
        topicourseURL = reverse('topicourse')
        params = {
            'topicourseID': self.topicourse.topicourseID,
            'topicourseTitle': "topicourse Title",
            'topicourseContent': "topicourse description",
            'topicourseTag': "tag1, tag2",
            'topicourseType': "type1",
            'topicourseLevel': 3,
        }

        response = self.client.post(topicourseURL, params)
        self.assertEquals(200, response.status_code, "post status errcode %d" %(response.status_code))
        ret = json.loads(response.content)
        self.assertEquals(errcode.topicourseLevelInvalid, ret["c"], "post errcode %d" %(ret["c"]))