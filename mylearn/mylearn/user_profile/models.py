from mongoengine import *
from django.db import models

# Create your models here.

class userPersonalProfile(EmbeddedDocument):
    aboutUserQuote = StringField(max_length=120)
    userEducationCredentials = StringField(max_length=120)
    userWorkCredentials = StringField(max_length=120)
    userLocation = StringField(max_length=120)

class user(Document):
    user_email = StringField(max_length=120, required=True)
    user_name = StringField(max_length=50)
    userPersonalProfile=EmbeddedDocumentField(userPersonalProfile)


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
    userSkypeID = StringField()
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

class Topiquiz(EmbeddedDocument):
    topiquizType = IntField()
    topiquizQuestion = StringField()
    topiquizOption = ListField(StringField())
    topiquizAnswer = StringField()
    topiquizExplanation = StringField()


class Topicourses(Document):
    topicourseUploadTimeStamp = LongField()
    topicourseCreatorUserID = ObjectIdField()
    #
    #topicoursesReview = ListField(EmbeddedDocumentField(TopicoursesReview))
    # topiquiz =

class TopicoursesDiscussionThread(Document):
    topicoursesID = ObjectIdField()
    topicoursesDiscussionTimeStamp = LongField()
    topicoursesDiscussionQuestionTitle = StringField()
    topicoursesDiscussionQuestionContent = StringField()
    topicoursesDiscussionCreatorUserID = ObjectIdField()

class TopicoursesDiscussionComment(Document):
    topicoursesID = ObjectIdField()
    topicoursesDiscussionID = ObjectIdField()
    topicoursesDiscussionReplyTimeStamp = LongField()
    #vote




