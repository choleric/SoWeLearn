from mongoengine import *
from django.db import models

from mylearn.apps import errcode

# Create your models here.

class UserVerified(EmbeddedDocument):
    IsVerified = BooleanField(default=False)
    verifiedTimeStamp = DateTimeField()
    verifiedStaffId = LongField()

    meta = {'allow_inheritance': True}

class UserEducationCredential(UserVerified):
    userEducationInfo = StringField()

class UserWorkCredential(UserVerified):
    userWorkInfo = StringField()

class UserPersonalProfile(Document):
    userID = LongField(primary_key=True)
    userSkypeID = StringField(max_length=40)
    aboutUserQuote = StringField()
    userEducationCredential = ListField(EmbeddedDocumentField(UserEducationCredential))
    userWorkCredential = ListField(EmbeddedDocumentField(UserWorkCredential))
    userLocation = StringField()

    #If user is tutor
    verifiedTutor = BooleanField()
    # only for tutor
    tutorTuitionTopics = StringField()
    tutorMiddleSchoolHourlyRate = LongField()
    tutorHighSchoolHourlyRate = LongField()
    tutorCollegeHourlyRate = LongField()