import json

from django.core.urlresolvers import reverse
from django.conf import settings

from ..projtest import BaseTest
from ..projtest import BaseTestUtil
from mylearn.apps import errcode

class YoutubeTestCase(BaseTest):
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

    def setUp(self) :
        super(YoutubeTestCase, self).setUp()
        self.__user = self._create_user_and_login()

    def tearDown(self) :
        self.client.post(reverse('account_signout_learn'))
        self.__user = None

    @property
    def user(self) :
        return self.__user

    def test_get_auth_url(self):
        auth_url = reverse('youtube_auth')
        response = self.client.get(auth_url)

        self.assertEquals(302, response.status_code,
                          "get auth url status errcode %d" %(response.status_code))
        self.assertTrue(0<response['Location'].find('www.google.com/accounts/AuthSubRequest'),
                          response['Location'])

    def test_upload_video_metadata(self):
        metaURL = reverse("youtube_upload_meta")
        params = {'auth_token': "1%2FJlB16DEhW61_Gwma6ObLWY3bmihXd0mFfHEOpGHI_0s",
                  'title': "Test Video",
                  'description': "This is a test video",
                  'keywords': "Test, keywords",
                  'access_control': 0}

        response = self.client.post(metaURL, params)
        self.assertEquals(200, response.status_code,
                          "upload metadata post status errcode %d" %(response.status_code))
        ret = json.loads(response.content)
        self.assertEquals(errcode.SUCCESS, ret["c"], "post metadata errcode %d" %(ret["c"]))

        data = ret["d"]
        self.assertTrue(len(getattr(data, "token"))>0, data)
