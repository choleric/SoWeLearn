import json

from django.core.urlresolvers import reverse
from django.conf import settings

from models import *
from .forms import UserQuoteForm
from ..projtest import BaseTest
from ..projtest import BaseTestUtil
from mylearn.apps import errcode
from .forms import UserProfileForm


class UserPersonalProfileTestCase(BaseTest):
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

    def _create_user_profile(self) :
        self.__profile = UserPersonalProfile(
                userID=self.user.pk,
                userEmail = 'test@test.com'
                )
        self.__profile.save()


    def setUp(self) :
        super(UserPersonalProfileTestCase, self).setUp()
        self.__user = self._create_user_and_login()
        self._create_user_profile()

    def tearDown(self) :
        self.profile.delete()
        self.client.post(reverse('account_signout_learn'))
        self.__user = None

    @property
    def user(self) :
        return self.__user

    @property
    def profile(self) :
        return self.__profile

    def test_profile_field_update(self) :
        profileURL = reverse("profile_url")
        # paramName, data
        expectedPairs = (
                ('skypeID', "13"),
                ('aboutUserQuote', ""),
                ('userLocation', "Somewhere"),
                )

        # update profile info
        profile = self.profile
        params = {}
        for paramName, data in expectedPairs :
            params[paramName] = data

        response = self.client.post(profileURL, params)
        self.assertEquals(200, response.status_code, "editProfile post status errcode %d" %(response.status_code))
        ret = json.loads(response.content)
        self.assertEquals(errcode.SUCCESS, ret["c"], "editProfile post errcode %d" %(ret["c"]))

        # check profile value
        response = self.client.get(profileURL)
        self.assertEquals(200, response.status_code, "editProfile get status errcode %d" %(response.status_code))
        ret = json.loads(response.content)
        self.assertEquals(errcode.SUCCESS, ret["c"], "editProfile get errcode %d" %(ret["c"]))

        profileData = ret["d"]
        for paramName, data in expectedPairs :
            self.assertEquals(data, profileData[paramName],
                    "profile data check field '%s' is %s, expected %s" %(paramName, profileData[paramName], data))

    def test_tutor_profile_field_update(self) :
        profileURL = reverse("profile_url")
        # paramName, data
        expectedPairs = (
                ('skypeID', "13"),
                ('aboutUserQuote', "About user"),
                ('userLocation', "Somewhere"),
                ('tutorTuitionAverageHourlyRate', {'tutorTuitionAverageHourlyRateMiddleSchool': 20})
                )

        #Set the user to be tutor
        self.__profile.verifiedTutor=True
        self.__profile.tutorTuitionAverageHourlyRate = {'tutorTuitionAverageHourlyRateMiddleSchool': 20}
        self.__profile.save()

        # update profile info
        profile = self.profile

        for paramName, data in expectedPairs :
            params = {}
            params[paramName] = data

            response = self.client.post(profileURL, params)
            self.assertEquals(200, response.status_code, "editProfile post status errcode %d" %(response.status_code))
            ret = json.loads(response.content)
            self.assertEquals(errcode.SUCCESS, ret["c"], "editProfile post errcode %d" %(ret["c"]))

            # check profile value
            response = self.client.get(profileURL)
            self.assertEquals(200, response.status_code, "editProfile get status errcode %d" %(response.status_code))
            ret = json.loads(response.content)
            self.assertEquals(errcode.SUCCESS, ret["c"], "editProfile get errcode %d" %(ret["c"]))

            profileData = ret["d"]
            self.assertEquals(data, profileData[paramName],
                    "profile data check field '%s' is %s, expected %s" %(paramName, profileData[paramName], data))

    def test_profile_2field_1none_update(self) :
        profileURL = reverse("profile_url")
        params = {"userSkypeID": "15", "aboutUserQuote": "This is quote from A"}
        response = self.client.post(profileURL, params)
        self.assertEquals(200, response.status_code, "post status errcode %d" %(response.status_code))
        ret = json.loads(response.content)
        self.assertEquals(errcode.SUCCESS, ret["c"], "post errcode %d" %(ret["c"]))

        # check update value
        response = self.client.get(profileURL)
        self.assertEquals(200, response.status_code, "get status errcode %d" %(response.status_code))
        ret = json.loads(response.content)
        self.assertEquals(errcode.SUCCESS, ret["c"], "get errcode %d" %(ret["c"]))

        profileData = ret["d"]
        for name,data in params.iteritems():
            v = profileData[name]
            self.assertEquals(data, v, "field '%s': %s, expected %s, json: %s" % (name, v, data, ret["d"]))


class UserPersonalProfileNotLoginTestCase(BaseTest):
    def test_no_login_redirect_to_login_url(self) :
        profileURL = reverse("profile_url")

        response = self.client.post(profileURL, {"skypeID" : 1})
        self.assertEquals(302, response.status_code, "editProfile no login status errcode %d" %(response.status_code))
        self.assertTrue(0 < response["location"].find(settings.LOGIN_URL),
                "editProfile no login location %s" %(response["location"]))

def display_all_profile():
    print '==========='
    for i in UserPersonalProfile.objects.all():
            print 'profile', i.userID, i.userSkypeID, i.userEmail
    print '==========='

class UserProfileFormTest(BaseTest):
    def test_profile(self):
        display_all_profile()
        params = {"userSkypeID": "15", "aboutUserQuote": "This is quote from A", 'userID':1, 'userEmail':'test@test.com'}
        profile = UserProfileForm(params)
        self.assertEqual( profile.is_valid(),True)
        profile.save()
        display_all_profile()

