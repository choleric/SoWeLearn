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

class UserTeachingProfile(Document):
    tutorTuitionTopics = StringField()
    tutorTuitionAverageHourlyRateMiddleSchool = LongField()
    tutorTuitionAverageHourlyRateHighSchool = LongField()
    tutorTuitionAverageHourlyRateCollege = LongField()

class TopicoursesReview(EmbeddedDocument):
    topicoursesReviewCreatedTimeStamp = LongField()
    topicoursesReviewCreatorUserID = ObjectIdField()
    topicoursesReviewContent = StringField()

class Topiquiz(EmbeddedDocument):
    topiquizType = IntField()
    topiquizQuestion = StringField()
    topiquizOption = ListField(StringField())
    topiquizAnswer = StringField()
    topiquizExplanation = StringField()
    topiquizCreatedTimeStamp = LongField()
    topiquizCreatorUserID = LongField()
    topiquizErrorFlag = BooleanField()
    topiquizErrorFlagUserID = ObjectIdField()
    topiquizErrorFlagTimeStamp = LongField()

class UserReview(Document):
    reviewedSubjectID = ObjectIdField()
    reviewedSubjectType = StringField() #topicourse, topiquit, discussion
    reviewCreatorUserID = ObjectIdField()
    reviewVote = IntField()
    reviewContent = StringField()

class Topicourses(Document):
    topicourseUploadTimeStamp = LongField()
    topicourseCreatorUserID = LongField()
    topicoursesTitle = StringField()
    #
    #topicoursesReview = ListField(EmbeddedDocumentField(TopicoursesReview))
    topiquiz = ListField(EmbeddedDocumentField(Topiquiz))

class TopicoursesDiscussionThread(Document):
    topicoursesID = ObjectIdField()
    topicoursesDiscussionCreatedTimeStamp = LongField()
    topicoursesDiscussionQuestionTitle = StringField()
    topicoursesDiscussionQuestionContent = StringField()
    topicoursesDiscussionCreatorUserID = LongField()

class TopicoursesDiscussionComment(Document):
    topicoursesID = ObjectIdField()
    topicoursesDiscussionID = ObjectIdField()
    topicoursesDiscussionParentID = ObjectIdField()

    #
    topicoursesDiscussionCommentCreatorUserID = LongField()

    topicoursesDiscussionReplyTimeStamp = LongField()
    #vote
    usefulnessVotesCount = IntField()

class UserAppointment(Document):
    #TO-DO
    userRequestStudentID = LongField()
    userRequestTutorID = LongField()

    userAppointmentDate = LongField()
    userAppointmentStartTime = LongField()
    userAppointmentDuration = LongField()
    userAppointmentTitle = StringField()
    userAppointmentCost = IntField()
    userAppointmentTutorMessage = StringField()
    userAppointmentStatus = BooleanField() # finished or not
    userAppointmentCreatedTimeStamp = LongField()

class UserRequest(EmbeddedDocument):
    userRequestTuitionLevel = StringField()
    userRequestTuitionSubject = StringField()
    userRequestTuitionLearningGoal = StringField()
    #userRequestTimeZone = StringField(max_length=64)
    userRequestTimePreference = StringField()
    userRequestDatePreference = StringField()
    userRequestOther = StringField()

class TutorReply(EmbeddedDocument):
    tutorReplyPriceQuote = IntField()
    tutorReplyTimeSlotList = ListField()
   # tutorReplyTimeZone = StringField()
    tutorReplyMessage = StringField()

class UserRequestTutor(Document):
    sessionID = LongField()
    userRequestStudentID = LongField()
    userRequestTutorID = LongField()
    createdTimeStamp = LongField()
    timeZone = StringField()
    userRequest = EmbeddedDocumentField(UserRequest)




