from django.db import models
from djangotoolbox.fields import EmbeddedModelField, ListField

# Create your models here.

class UserVerified(models.Model):
    IsVerified = models.BooleanField(default=False)
    verifiedTimeStamp = models.DateTimeField(auto_now=True)
    verifiedStaffId = models.BigIntegerField()

class UserEducationCredential(UserVerified):
    userEducationInfo = models.CharField(max_length=100)

class UserWorkCredential(UserVerified):
    userWorkInfo = models.CharField(max_length=100)

class TutorHourlyRate(models.Model):
    tutorTuitionAverageHourlyRateMiddleSchool = models.PositiveSmallIntegerField(blank=True)
    tutorTuitionAverageHourlyRateHighSchool = models.PositiveSmallIntegerField(blank=True)
    tutorTuitionAverageHourlyRateCollege = models.PositiveSmallIntegerField(blank=True)

class UserPersonalProfile(models.Model):
    userID = models.BigIntegerField(primary_key=True)
    skypeID = models.CharField(max_length=20, blank=True)
    aboutUserQuote = models.CharField(blank=True, max_length=100)
    userEducationCredential = ListField(EmbeddedModelField('UserEducationCredential'), blank=True)
    userWorkCredential = ListField(EmbeddedModelField('UserWorkCredential'), blank=True)
    userLocation = models.CharField(max_length=50)
    #whether user is verified as a tutor
    verifiedTutor= models.BooleanField(default=False)
    #Only available if user is verified as a tutor
    tutorTuitionTopics = ListField()
    tutorTuitionAverageHourlyRate = EmbeddedModelField('TutorHourlyRate')
