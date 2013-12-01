from mongoengine import *
from django.db import models

class Profile(UserenaLanguageBaseProfile):

    gender = models.PositiveSmallIntegerField(_('gender'),
                                              choices=GENDER_CHOICES,
                                              blank=True,
                                              null=True)
    website = models.URLField(_('website'), blank=True)
    location =  models.CharField(_('location'), max_length=255, blank=True)
    birth_date = models.DateField(_('birth date'), blank=True, null=True)
    about_me = models.TextField(_('about me'), blank=True)  
    
class userVerified(EmbeddedDocument):
    IsVerified = BooleanField(default=False)
    verifiedTimeStamp = LongField()
    verifiedStaffId = ObjectIdField()  
    
    meta = {'allow_inheritance': True}  
    
class UserEducationCredential(userVerified):
    userEducationInfo = StringField()
       
class UserWorkCredential(userVerified):
    userWorkInfo = StringField()
    
class userPersonalProfile(Document):
    userSkypeID ＝ StringField()
    aboutUserQuote = StringField()
    userEducationCredential = ListField(EmbeddedDocumentField(UserEducationCredential))
    userWorkCredential = ListField(EmbeddedDocumentField(UserWorkCredential))
    userLocation = StringField()
    
class userTeachingProfile(Document):
    tutorTuitionTopics = StringField()    
    tutorTuitionAverageHourlyRateMiddleSchool = LongField()
    tutorTuitionAverageHourlyRateHighSchool = LongField()
    tutorTuitionAverageHourlyRateCollege = LongField()

class TopicoursesReview(EmbeddedDocument):
    topicoursesReviewTimeStamp = LongField()
    topicoursesReviewCreatorUserID = ObjectIdField()
    topicoursesReviewContent = StringField()
    
class Topicourses(Document):
    topicourseUploadTimeStamp = LongField()
    topicourseCreatorUserID = ObjectIdField()
    #
    topicoursesReview = ListField(EmbeddedDocumentField(TopicoursesReview))
    
class TopicoursesDiscussionThread():
    TopicoursesID = ObjectIdField()
    topicoursesDiscussionTimeStamp = LongField()
    topicoursesDiscussionQuestionTitle = StringField()
    topicoursesDiscussionQuestionContent = StringField()