from django.db import models
from djangotoolbox.fields import EmbeddedModelField, ListField
from mylearn.apps import errcode

# Create your models here.

class UserVerified(models.Model):
    IsVerified = models.BooleanField(default=False)
    verifiedTimeStamp = models.DateTimeField(auto_now=True)
    verifiedStaffId = models.BigIntegerField(null=True)

class UserEducationCredential(UserVerified):
    userEducationInfo = models.CharField(max_length=100,
            error_messages={
                "invalid" :errcode.profileEducationCredentialInvalid
            })

class UserWorkCredential(UserVerified):
    userWorkInfo = models.CharField(max_length=100,
            error_messages={
                "invalid" :errcode.profileEducationCredentialInvalid
            })

class TutorHourlyRate(models.Model):
    tutorTuitionAverageHourlyRateMiddleSchool = models.PositiveSmallIntegerField(null=True,
            error_messages={
                "invalid" : errcode.profileTutorHourlyRateInvalid,
            })
    tutorTuitionAverageHourlyRateHighSchool = models.PositiveSmallIntegerField(null=True,
            error_messages={
                "invalid" : errcode.profileTutorHourlyRateInvalid,
            })
    tutorTuitionAverageHourlyRateCollege = models.PositiveSmallIntegerField(null=True,
            error_messages={
                "invalid" : errcode.profileTutorHourlyRateInvalid,
            })

class UserPersonalProfile(models.Model):
    userID = models.BigIntegerField(primary_key=True)

    skypeID = models.CharField(max_length=200,
            blank = True,
            error_messages={
        "max_length" : str(errcode.profileQuoteInvalid),
    })
    aboutUserQuote = models.CharField(max_length=200,
            blank = True,
            error_messages={
        "invalid" : errcode.profileQuoteInvalid,
    })

    #
    userEducationCredential = ListField(EmbeddedModelField('UserEducationCredential'), blank=True)
    userWorkCredential = ListField(EmbeddedModelField('UserWorkCredential'), blank=True)
    userLocation = models.CharField(max_length=50,
            blank=True,
            error_messages={
                "max_length" : errcode.profilelocationInvalid,
            })
    #whether user is verified as a tutor
    verifiedTutor= models.BooleanField(default=False)
    #Only available if user is verified as a tutor
    tutorTuitionTopics = ListField(blank=True)
    tutorTuitionAverageHourlyRate = EmbeddedModelField('TutorHourlyRate', null=True, blank=True)
