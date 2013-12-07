from mongoengine import *
from django.db import models

# Create your models here.

class userPersonalProfile(EmbeddedDocument):
    aboutUserQuote = StringField(max_length=120)
    userEducationCredentials = StringField(max_length=120)
    userWorkCredentials = StringField(max_length=120)
    userLocation = StringField(max_length=120)

class user(Document):
    userEmail = StringField(max_length=120, required=True,unique=True)
    userName = StringField(max_length=50)
    #userPersonalProfile=EmbeddedDocumentField(userPersonalProfile)
#
class UserVerified(EmbeddedDocument):
    IsVerified = BooleanField(default=False)
    verifiedTimeStamp = LongField()
    verifiedStaffId = LongField()

    meta = {'allow_inheritance': True}

class UserEducationCredential(UserVerified):
    userEducationInfo = StringField()

class UserWorkCredential(UserVerified):
    userWorkInfo = StringField()

class UserPersonalProfile(Document):
    userEmail = StringField(unique=True)
    userSkypeID = StringField()
    aboutUserQuote = StringField()
    userEducationCredential = ListField(
                                EmbeddedDocumentField(UserEducationCredential))
    userWorkCredential = ListField(EmbeddedDocumentField(UserWorkCredential))
    userLocation = StringField()

    # only for tutor
    tutorTuitionTopics = StringField()
    tutorTuitionAverageHourlyRateMiddleSchool = LongField()
    tutorTuitionAverageHourlyRateHighSchool = LongField()
    tutorTuitionAverageHourlyRateCollege = LongField()

    def change_about_user_quote(self, new_quote):
        self.aboutUserQuote = new_quote
        self.save()

    def change_user_skypeid(self, new_skypeid):
        self.userSkypeID = new_skypeid
        self.save()

    def change_education_info2(self, new_education_info):
        #self.userEducationCredential = new_education_info
        #education = UserEducationCredential()
        for i in range(0,len(new_education_info)):
            self.userEducationCredential[i].userEducationInfo=new_education_info[i]['userEducationInfo']
            self.userEducationCredential[i].IsVerified=new_education_info[i]['IsVerified']
            self.userEducationCredential[i].verifiedTimeStamp=new_education_info[i]['verifiedTimeStamp']
            self.userEducationCredential[i].verifiedStaffId=new_education_info[i]['verifiedStaffId']
        self.save()

    def change_education_info(self, new_education_info):
        #self.userEducationCredential = new_education_info
        #education = UserEducationCredential()
        for i in range(0,len(new_education_info)):
            self.userEducationCredential[i]=UserEducationCredential(**new_education_info[i])
        self.save()