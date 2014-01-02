import json
from models import *
from django.core.urlresolvers import reverse
from django.conf import settings

from .forms import UserQuoteForm
from ..projtest import BaseTest
from ..projtest import BaseTestUtil
from mylearn.apps import errcode


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
                userID=self.user.pk
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

    def test_profile_2field_1none_update(self) :
        profileURL = reverse("profile_url")
        params = {"skypeID": "15", "quote": "This is quote from A"}
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


    def test_change_about_user_quote(self):
        #create test user
        new_quote = 'new quote'

        #test before changing
        self.assertNotEqual(self.profile.aboutUserQuote, new_quote)

        self.profile.change_about_user_quote(new_quote)

        #test after changing
        self.assertEqual(self.profile.aboutUserQuote, new_quote)

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
        
        self.profile.update(userEducationCredential=userEducationCredential)

        new_userEducationCredential=[]
        for i in range(0,2):
            educationCredential={}
            educationCredential['userEducationInfo']='new education info'
            educationCredential['IsVerified']=True
            educationCredential['verifiedTimeStamp']=11110
            educationCredential['verifiedStaffId']=11
            new_userEducationCredential.append(educationCredential)
        #test before changing
        user = UserPersonalProfile(userID=self.profile.userID)
        for i in range(0,1):
            self.assertNotEqual(user.userEducationCredential[i].userEducationInfo,new_userEducationCredential[i]['userEducationInfo'])

        user.change_education_info(new_userEducationCredential)
        #test after changing
        newuser = UserPersonalProfile.objects.get(userEmail=self.user.pk)
        for i in range(0,1):
            self.assertEqual(newuser.userEducationCredential[i].userEducationInfo,new_userEducationCredential[i]['userEducationInfo'])

    def test_change_work_info(self):
        #create test user
        userWorkCredential=[]
        for i in range(0,2):
            workCredential={}
            workCredential['userWorkInfo']='test work info'
            workCredential['IsVerified']=True
            workCredential['verifiedTimeStamp']=22220+i
            workCredential['verifiedStaffId']=22
            userWorkCredential.append(workCredential)
        UserPersonalProfile.objects.create(userSkypeID='skypei_id001', aboutUserQuote='my quote', userEmail='009',userWorkCredential=userWorkCredential)

        new_userWorkCredential=[]
        for i in range(0,1):
            workCredential={}
            workCredential['userWorkInfo']='new work info'
            workCredential['IsVerified']=True
            workCredential['verifiedTimeStamp']=11110+i
            workCredential['verifiedStaffId']=11
            new_userWorkCredential.append(workCredential)
        #test before changing
        user = UserPersonalProfile.objects.get(userEmail=self.user.pk)
        for i in range(0,1):
            self.assertNotEqual(user.userWorkCredential[i].userWorkInfo,new_userWorkCredential[i]['userWorkInfo'])

        user.change_work_info(new_userWorkCredential)
        #test after changing
        newuser = UserPersonalProfile.objects.get(userEmail=self.user.pk)
        for i in range(0,1):
            self.assertEqual(newuser.userWorkCredential[i].userWorkInfo,new_userWorkCredential[i]['userWorkInfo'])



class UserProfileFormTestCase(BaseTest):
    def test_user_quote_form(self):
        quote = UserQuoteForm(data={'aboutUserQuote': 'hello world'})

        self.assertEqual(quote.is_valid(), False)

    def test_modify_user_quote(self):
        response = self.client.post('/modify-user-quote/',{'aboutUserQuote': 'hello'})

        self.assertEqual(response.status_code, 302)


    def test_modify_user_quote_length(self):
        response = self.client.post('/modify-user-quote/',{'aboutUserQuote': 'hello world'})

        quote = UserQuoteForm(data={'aboutUserQuote': 'hello world'})
        self.assertEqual(quote.is_valid(), False)

    def test_modify_user_quote(self):
        response = self.client.post('/modify-user-quote/',{'aboutUserQuote': 'hello'})
        self.assertEqual(response.status_code, 200)
        responseDict = json.loads(response.content)
        self.assertEquals(responseDict['success'], True)

    def test_modify_user_quote_length(self):
        response = self.client.post('/modify-user-quote/',{'aboutUserQuote': 'hello world'})
        self.assertEqual(response.status_code, 200)
        responseDict = json.loads(response.content)
        self.assertEquals(responseDict['success'], False)

    def test_modify_user_quote_empty(self):
        response = self.client.post('/modify-user-quote/',{'aboutUserQuote': ''})

        self.assertEqual(response.status_code, 200)
        responseDict = json.loads(response.content)
        self.assertEquals(responseDict['success'], False)

    def test_modify_user_quote_invalid_request(self):
        response = self.client.get('/modify-user-quote/',{'aboutUserQuote': 'hello world'})
        self.assertEqual(response.status_code, 404, response.status_code)

    def test_modify_work_and_edu_empty(self):
        response = self.client.post('/modify_work_and_education_credential/',{'userEducationCredential': '','userWorkCredential':''})
        self.assertEqual(response.status_code, 200)
        responseDict = json.loads(response.content)
        self.assertEquals(responseDict['success'], False)


class UserPersonalProfileNotLoginTestCase(BaseTest):
    def test_no_login_redirect_to_login_url(self) :
        profileURL = reverse("profile_url")

        response = self.client.post(profileURL, {"skypeID" : 1})
        self.assertEquals(302, response.status_code, "editProfile no login status errcode %d" %(response.status_code))
        self.assertTrue(0 < response["location"].find(settings.LOGIN_URL),
                "editProfile no login location %s" %(response["location"]))
