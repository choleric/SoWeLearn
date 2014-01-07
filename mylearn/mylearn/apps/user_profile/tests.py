import json

from django.core.urlresolvers import reverse
from django.conf import settings

from ..projtest import BaseTest
from ..projtest import BaseTestUtil
from mylearn.apps import errcode
from models import *
from .forms import UserProfileForm, UserEducationForm

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

    def test_get_personal_profile(self):
        profileURL = reverse("personal_profile_url")

        response = self.client.get(profileURL)
        self.assertEquals(200, response.status_code, "get status errcode %d" %(response.status_code))
        ret = json.loads(response.content)
        self.assertEquals(errcode.SUCCESS, ret["c"], "get errcode %d" %(ret["c"]))

    def _update_result_test(self, profileURL, params):

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

    def test_profile_field_update(self) :
        profileURL = reverse("personal_profile_url")
        # paramName, data
        expectedPairs = (
                ('userSkypeID', "13"),
                ('aboutUserQuote', "quote"),
                ('userLocation', "Somewhere"),
                )

        # update profile info
        profile = self.profile
        params = {}
        for paramName, data in expectedPairs :
            params[paramName] = data

        self._update_result_test(profileURL, params)

        expectedPairs_new = (
                ('userSkypeID', "14"),
                ('aboutUserQuote', "quote"),
                ('userLocation', "Somewhere"),
                )

        #When only 1 field is being updated, make sure that the others are not overwritten!
        params_new={}
        params_new['userSkypeID']="14"

        response = self.client.post(profileURL, params_new)
        self.assertEquals(200, response.status_code, "editProfile post status errcode %d" %(response.status_code))
        ret = json.loads(response.content)
        self.assertEquals(errcode.SUCCESS, ret["c"], "editProfile post errcode %d" %(ret["c"]))

        # check profile value
        response = self.client.get(profileURL)
        self.assertEquals(200, response.status_code, "editProfile get status errcode %d" %(response.status_code))
        ret = json.loads(response.content)
        self.assertEquals(errcode.SUCCESS, ret["c"], "editProfile get errcode %d" %(ret["c"]))

        profileData_new = ret["d"]
        for paramName, data in expectedPairs_new :
            self.assertEquals(data, profileData_new[paramName],
                    "profile data check field '%s' is %s, expected %s" %(paramName, profileData_new[paramName], data))

    def test_profile_2field_1none_update(self) :
        profileURL = reverse("personal_profile_url")
        params = {"userSkypeID": "15", "aboutUserQuote": "This is quote from A"}

        self._update_result_test(profileURL, params)

    def test_profile_update_error(self):
        profileURL = reverse("personal_profile_url")
        # paramName, data
        expectedPairs = (
                ('userSkypeID', "This_user_skype_ID_is_going_to_be_too_long"),
                ('aboutUserQuote', "quote"),
                ('userLocation', "Somewhere"),
                )

        # update profile info
        profile = self.profile
        params = {}
        for paramName, data in expectedPairs :
            params[paramName] = data

        response = self.client.post(profileURL, params)
        self.assertEquals(200, response.status_code, "post status errcode %d" %(response.status_code))
        ret = json.loads(response.content)
        self.assertEquals(errcode.profileSkypeIDInvalid, ret["c"], "post errcode %d" %(ret["c"]))

    def test_edu_profile_update(self):
        profileURL = reverse("personal_profile_url")
        params = {'userEducationInfo':"EducationInformation"}

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
        v = profileData['userEducationCredential'][0]
        for name,data in params.iteritems():
            self.assertEquals(data, v[name], "field '%s': %s, expected %s, json: %s" % (name, v, data, ret["d"]))

        #now edit the edu info
        params_edit = {'userEducationInfo':"new info", 'position': 0}
        response = self.client.post(profileURL, params_edit)
        self.assertEquals(200, response.status_code, "post status errcode %d" %(response.status_code))
        ret = json.loads(response.content)
        self.assertEquals(errcode.SUCCESS, ret["c"], "post errcode %d" %(ret["c"]))

         # check update value
        response = self.client.get(profileURL)
        self.assertEquals(200, response.status_code, "get status errcode %d" %(response.status_code))
        ret = json.loads(response.content)
        self.assertEquals(errcode.SUCCESS, ret["c"], "get errcode %d" %(ret["c"]))

        profileData = ret["d"]
        v = profileData['userEducationCredential'][0]
        self.assertEqual("new info", v['userEducationInfo'], v)

    def test_work_profile_update(self):
        profileURL = reverse("personal_profile_url")
        params = {'userWorkInfo':"part-time tutor"}

        response = self.client.post(profileURL, params)
        self.assertEquals(200, response.status_code, "post status errcode %d" %(response.status_code))
        ret = json.loads(response.content)
        self.assertEquals(errcode.SUCCESS, ret["c"], "post errcode %d" %(ret["c"]))

        # check update value
        response = self.client.get(profileURL)
        self.assertEquals(200, response.status_code, "get status errcode %d" %(response.status_code))
        ret = json.loads(response.content)
        self.assertEquals(errcode.SUCCESS, ret["c"], "get errcode %d" %(ret["c"]))

        # returned data as a list
        profileData = ret["d"]
        v = profileData['userWorkCredential'][0]
        for name,data in params.iteritems():
            self.assertEquals(data, v[name], "field '%s': %s, expected %s, json: %s" % (name, v, data, ret["d"]))

    def test_unverified_tutor(self):
        profileURL = reverse("tutor_profile_url")

        response = self.client.get(profileURL)
        self.assertEquals(200, response.status_code, "get status errcode %d" %(response.status_code))
        ret = json.loads(response.content)
        self.assertEquals(errcode.UserNotVerifiedAsTutor, ret["c"], "get errcode %d" %(ret["c"]))

    def test_tutor_profile_field_update(self) :
        profileURL = reverse("tutor_profile_url")
        # paramName, data
        expectedPairs = (
                ('tutorTuitionTopics', "Chemistry"),
                ('tutorMiddleSchoolHourlyRate', 20),
                ('tutorHighSchoolHourlyRate', 30),
                ('tutorCollegeHourlyRate', 40),
                )

        #Set the user to be tutor
        self.__profile.verifiedTutor=True
        self.__profile.tutorTuitionAverageHourlyRateHighSchool=20
        self.__profile.save()

        # update profile info
        profile = self.profile

        for paramName, data in expectedPairs :
            params = {}
            params[paramName] = data

            #Test post data and check status, get the data
            #Make sure the update has been done
            self._update_result_test(profileURL, params)

    def test_tutor_profile_update_error(self):
        #Set the user to be tutor
        self.__profile.verifiedTutor=True
        self.__profile.save()

        profileURL = reverse("tutor_profile_url")

        params={}
        params['tutorMiddleSchoolHourlyRate'] = "Invalid"

        response = self.client.post(profileURL, params)
        self.assertEquals(200, response.status_code, "post status errcode %d" %(response.status_code))
        ret = json.loads(response.content)
        self.assertEquals(errcode.middleSchoolHourlyRateInvalid, ret["c"], "post errcode %d" %(ret["c"]))


class UserPersonalProfileNotLoginTestCase(BaseTest):
    def test_no_login_redirect_to_login_url(self) :
        profileURL = reverse("personal_profile_url")

        response = self.client.post(profileURL, {"skypeID" : 1})
        self.assertEquals(302, response.status_code, "editProfile no login status errcode %d" %(response.status_code))
        self.assertTrue(0 < response["location"].find(settings.LOGIN_URL),
                "editProfile no login location %s" %(response["location"]))

class UserProfileFormTest(BaseTest):
    def test_user_profile(self):
        #test creating a profile via form
        params = {"userSkypeID": "15", "aboutUserQuote": "This is quote from A"}
        profile = UserProfileForm(params)
        self.assertEqual(profile.is_valid(),True)
        profile.instance.userID = 1
        profile.save()
        user = UserPersonalProfile.objects.get(userID = 1)
        self.assertEqual(user.userSkypeID, '15', user)
        self.assertEqual(user.aboutUserQuote, 'This is quote from A', user)

        #test update selected fields of a form
        update_pramas = {"userSkypeID" : "16"}
        profile_update = UserProfileForm(update_pramas)
        #profile_update.instance.userID = 1
        if profile_update.is_valid():
            profile_update.instance.userID = 1
            profile_update.save()
        user_update = UserPersonalProfile.objects.get(userID = 1)
        self.assertEqual(user_update.userSkypeID, '16', user)
        self.assertEqual(user_update.aboutUserQuote, 'This is quote from A', user)

    def test_user_edu_profile(self):
        #test creating a profile via form
        params = {'userEducationInfo':"EducationInformation"}
        parent_profile = UserPersonalProfile(userID = 2)
        parent_profile.save()
        profile = UserEducationForm(parent_document = parent_profile, data = params)
        self.assertEqual(profile.is_valid(), True)
        profile.save()
        user = UserPersonalProfile.objects.get(userID = 2)
        self.assertEqual(user.userEducationCredential[0].userEducationInfo,
                         "EducationInformation", user.userEducationCredential)

