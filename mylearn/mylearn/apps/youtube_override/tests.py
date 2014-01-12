import json

from django.core.urlresolvers import reverse
from django_youtube.models import Video

from ..projtest import BaseTest
from ..projtest import BaseTestUtil
from mylearn.apps import errcode
from ...settings import YOUTUBE_UPLOAD_REDIRECT_URL
from .forms import YoutubeMetadataForm

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

    def test_upload_video_metadata(self):
        metaURL = reverse("youtube_upload_meta")
        params = {'title': "Test Video",
                  'description': "This is a test video",
                  'keywords': "Test, keywords",
                  'access_control': 0}

        response = self.client.post(metaURL, params)
        self.assertEqual(200, response.status_code,
                          "upload metadata post status errcode %d" %(response.status_code))
        ret = json.loads(response.content)
        self.assertEqual(errcode.SUCCESS, ret["c"], "post metadata errcode %d" %(ret["c"]))

        data = ret["d"]
        self.assertTrue(len(data.get("token"))>0, data)
        self.assertTrue(len(data.get("post_url"))>0, data)
        self.assertTrue(len(data.get("next_url"))>0, data)

    def test_upload_return(self):
        #Important: the test depends on video_id that is actually saved on youtube!
        retURL = reverse('youtube_upload_return')
        params = {"status": 200,
                  "id": "iddXKy_zAkI"}
        response = self.client.get(retURL, params)
        self.assertEqual(302, response.status_code,
                          "upload return status errcode %d" %(response.status_code))
        self.assertTrue(0<response['Location'].find(YOUTUBE_UPLOAD_REDIRECT_URL),
                        "upload return url %s" %response['Location'])

        #Test if the model is working correctly
        video = Video.objects.get(video_id = "iddXKy_zAkI")
        self.assertEqual(video.user.pk, 1)

    def test_return_private_video(self):
        retURL = reverse('youtube_upload_return')
        params = {"status": 200,
                  "id": "mL2wHL-17A0"}
        response = self.client.get(retURL, params)
        self.assertEqual(302, response.status_code,
                          "upload return status errcode %d" %(response.status_code))
        self.assertTrue(0<response['Location'].find(YOUTUBE_UPLOAD_REDIRECT_URL),
                        "upload return url %s" %response['Location'])

        #Test if the model is working correctly
        video = Video.objects.get(video_id = "mL2wHL-17A0")
        self.assertEqual(video.user.pk, 1)

    def test_get_private_video(self):
        videoURL = reverse('youtube_video', kwargs={"video_id": "mL2wHL-17A0"})
        response = self.client.get(videoURL)

        self.assertEqual(200, response.status_code,
                        "get video url return status errcode %d" %(response.status_code))
        ret = json.loads(response.content)
        self.assertEqual(errcode.SUCCESS, ret["c"], "post metadata errcode %d" %(ret["c"]))

        data = ret["d"]
        self.assertTrue(len(data.get("video_src"))>0, data)
        self.assertTrue(len(data.get("width"))>0, data)

    def test_upload_return_error(self):
        retURL = reverse('youtube_upload_return')
        params = {"status": 200,
                  "id": "wrongID"}
        response = self.client.get(retURL, params)
        self.assertEqual(200, response.status_code,
                          "upload return status code %d" %(response.status_code))
        ret = json.loads(response.content)
        self.assertEqual(errcode.YoutubeUploadVideoError, ret["c"],
                         "upload return errcode %d" %(ret["c"]))

    def test_upload_return_wrong_status(self):
        retURL = reverse('youtube_upload_return')
        params = {"status": 400,
                  "id": "iddXKy_zAkI"}
        response = self.client.get(retURL, params)
        self.assertEqual(200, response.status_code,
                          "upload return status code %d" %(response.status_code))
        ret = json.loads(response.content)
        self.assertEqual(errcode.YoutubeUploadVideoError, ret["c"],
                         "upload return errcode %d" %(ret["c"]))

class YoutubeFormTest(BaseTest):
    def test_metadata_form(self):
        params = {'title': "Test Video",
                  'description': "This is a test video",
                  'keywords': "Test, keywords",
                  'access_control': 0}
        videoMetadata = YoutubeMetadataForm(params)
        self.assertEqual(videoMetadata.is_valid(), True)
        videoMetadata.user = 1
        videoMetadata.video_id = "This is the video id"