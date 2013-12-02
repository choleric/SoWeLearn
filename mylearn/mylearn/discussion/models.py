from mongoengine import *
from django.db import models

# Create your models here.


class UserReview(Document):
    reviewedSubjectID = ObjectIdField()
    reviewedSubjectType = StringField() #topicourse, topiquit, discussion
    reviewCreatorUserID = ObjectIdField()
    reviewVote = IntField()
    reviewContent = StringField()

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

