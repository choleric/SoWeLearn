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

