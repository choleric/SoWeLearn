from mongoengine import *
from django.db import models

# Create your models here.

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
    userID = LongField(primary_key=True)
    userSkypeID = StringField()
    aboutUserQuote = StringField()
    userEducationCredential = ListField(
                                EmbeddedDocumentField(UserEducationCredential))
    userWorkCredential = ListField(EmbeddedDocumentField(UserWorkCredential))
    userLocation = StringField()

    #If user is tutor
    verifiedTutor = BooleanField(default=False)
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

    def change_education_info(self, new_education_info):
        self.update(pull_all__userEducationCredential=self.userEducationCredential)
        self.reload()
        for education_info in new_education_info:
            self.userEducationCredential.append(UserEducationCredential(**education_info))
        self.save()

    def change_work_info(self, new_work_info):
        self.update(pull_all__userWorkCredential=self.userWorkCredential)
        self.reload()
        for work_info in new_work_info:
            self.userWorkCredential.append(UserWorkCredential(**work_info))
        self.save()

    def change_tutorTuitionTopics(self, new_tutorTuitionTopics):
        self.tutorTuitionTopics = new_tutorTuitionTopics
        self.save()

    def change_tutorTuitionAverageHourlyRateMiddleSchool(self, new_tutorAverageRate):
        self.tutorTuitionAverageHourlyRateMiddleSchool = new_tutorAverageRate
        self.save()
    def tutorTuitionAverageHourlyRateHighSchool(self, new_tutorAverageRate):
        self.tutorTuitionAverageHourlyRateHighSchool = new_tutorAverageRate
        self.save()
    def tutorTuitionAverageHourlyRateCollege(self, new_tutorAverageRate):
        self.tutorTuitionAverageHourlyRateCollege = new_tutorAverageRate
        self.save()