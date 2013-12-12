from mongoengine import *
from django.db import models
import datetime

# Create your models here.

# put all vote into this table
class UserReview(Document):
    reviewedSubjectID = ObjectIdField()
    reviewedSubjectType = StringField() #topicourse, topiquit, discussion
    reviewCreatorUserID = ObjectIdField()
    reviewVote = IntField()
    reviewContent = StringField()

class TopicoursesReview(EmbeddedDocument):
    topicoursesReviewCreatedTimeStamp = DateTimeField(default=datetime.datetime.now)
    topicoursesReviewCreatorUserID = ObjectIdField()
    topicoursesReviewContent = StringField()

class Topiquiz(EmbeddedDocument):
    topiquizId = ObjectIdField()
    topiquizType = IntField()
    topiquizQuestion = StringField()
    topiquizOption = ListField(StringField())
    topiquizAnswer = StringField()
    topiquizExplanation = StringField()
    topiquizCreatedTimeStamp = DateTimeField(default=datetime.datetime.now)
    topiquizCreatorUserID = LongField(required=True)
    topiquizErrorFlag = BooleanField()
    topiquizErrorFlagUserID = ObjectIdField()
    topiquizErrorFlagTimeStamp = DateTimeField()

class Topicourses(Document):
    topicourseId = StringField()
    topicoursesUploadTimeStamp = DateTimeField(default=datetime.datetime.now)
    topicoursesCreatorUserID = LongField(required=True)
    topicoursesTitle = StringField(required=True)
    topicoursesContent = StringField()
    topicourseTag = ListField(StringField())
    topicourseType = StringField()
    topicourseLevel = StringField()
    #
    topicoursesReview = ListField(EmbeddedDocumentField(TopicoursesReview))
    topiquiz = ListField(EmbeddedDocumentField(Topiquiz))

    def change_topicourses_title(self, new_title):
        self.topicoursesTitle = new_title
        self.save()

    # TODO
    def update_topiquiz(self, topiquiz):
        newtopiquiz = Topiquiz(**topiquiz)
        quiz_idx = -1
        for quiz in self.topiquiz:
            if quiz.topiquizId == newtopiquiz.topiquizId:
                quiz_idx = self.topiquiz.index(quiz)
                break
        if quiz_idx >= 0:
            self.topiquiz[quiz_idx] = newtopiquiz
            self.save()

    def upload_topiquiz(self, topiquiz):
         self.topiquiz.append(Topiquiz(**topiquiz))
         self.save()

    def change_tag(self,new_tag):
        self.update(pull_all__topicourseTag=self.topicourseTag)
        self.reload()
        for tag in new_tag:
            self.topicourseTag.append(tag)
        self.save()

