from mongoengine import *
from django.db import models

# Create your models here.

# put all vote into this table
class UserReview(Document):
    reviewedSubjectID = ObjectIdField()
    reviewedSubjectType = StringField() #topicourse, topiquit, discussion
    reviewCreatorUserID = ObjectIdField()
    reviewVote = IntField()
    reviewContent = StringField()


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

class Topicourses(Document):
    topicourseUploadTimeStamp = LongField()
    topicourseCreatorUserID = LongField()
    topicoursesTitle = StringField()
    #
    #topicoursesReview = ListField(EmbeddedDocumentField(TopicoursesReview))
    topiquiz = ListField(EmbeddedDocumentField(Topiquiz))
