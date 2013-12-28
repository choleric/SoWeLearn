from mongoengine import *
from django.db import models

# Create your models here.

class userPersonalProfile(EmbeddedDocument):
    aboutUserQuote = StringField(max_length=120)
    userEducationCredentials = StringField(max_length=120)
    userWorkCredentials = StringField(max_length=120)
    userLocation = StringField(max_length=120)

class User(Document):
    userEmail = StringField(max_length=120, required=True,unique=True)
    userFirstName = StringField(max_length=50)
    userLastName = StringField(max_length=50)
    #userPersonalProfile=EmbeddedDocumentField(userPersonalProfile)

    def user_signup(self, userEmail, userFirstName, userLastName):
        self.userEmail = userEmail
        self.userFirstName = userFirstName
        self.userLastName = userLastName
        self.create()
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
    userID = LongField(unique = True, required = True, primary_key = True)
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
