import json
from models import *
from .forms import UserQuoteForm
from ..projtest import BaseTest


class UserPersonalProfileTestCase(BaseTest):

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
        for i in range(0,2):
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
        user = UserPersonalProfile.objects.get(userEmail='009')
        for i in range(0,1):
            self.assertNotEqual(user.userWorkCredential[i].userWorkInfo,new_userWorkCredential[i]['userWorkInfo'])

        user.change_work_info(new_userWorkCredential)
        #test after changing
        newuser = UserPersonalProfile.objects.get(userEmail='009')
        for i in range(0,1):
            self.assertEqual(newuser.userWorkCredential[i].userWorkInfo,new_userWorkCredential[i]['userWorkInfo'])



class UserProfileFormTestCase(BaseTest):
    def test_user_quote_form(self):
        quote = UserQuoteForm(data={'aboutUserQuote': 'hello world'})
        print quote
        self.assertEqual(quote.is_valid(), False)

    def test_modify_user_quote(self):
        response = self.client.post('/modify-user-quote/',{'aboutUserQuote': 'hello'})
        print response.status_code
        self.assertEqual(response.status_code, 302)
        print response

    def test_modify_user_quote_length(self):
        response = self.client.post('/modify-user-quote/',{'aboutUserQuote': 'hello world'})
        print response.status_code
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
        print response.status_code
        self.assertEqual(response.status_code, 200)
        responseDict = json.loads(response.content)
        self.assertEquals(responseDict['success'], False)

    def test_modify_user_quote_invalid_request(self):
        response = self.client.get('/modify-user-quote/',{'aboutUserQuote': 'hello world'})
        print response.status_code
        print response
        self.assertEqual(response.status_code, 404)

    def test_modify_work_and_edu_empty(self):
        response = self.client.post('/modify_work_and_education_credential/',{'userEducationCredential': '','userWorkCredential':''})
        self.assertEqual(response.status_code, 200)
        responseDict = json.loads(response.content)
        self.assertEquals(responseDict['success'], False)

