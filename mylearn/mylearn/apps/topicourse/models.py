import datetime
from django.template.defaultfilters import slugify
from mongoengine import *
from django.db import models

from mylearn.apps import errcode


# Create your models here.

class Topicourse(models.Model):
    LEVELS=(
        (0, 'Middle School'),
        (1, 'High School'),
        (2, 'College'),
    )
    topicourseID = models.AutoField(primary_key=True)
    topicourseUploadTimeStamp = models.DateTimeField(auto_created=True, auto_now_add=True)
    topicourseCreatorUserID = models.BigIntegerField()
    topicourseVideoID = models.CharField(unique=True, max_length=200)
    topicourseTitle = models.CharField(
        max_length=200,
        blank=True,
        error_messages={
            "invalid": errcode.topicourseTitleInvalid,
            })
    topicourseContent = models.CharField(
        max_length=1000,
        blank=True,
        error_messages={
            "invalid": errcode.topicourseContentInvalid,
            })
    topicourseTag = models.CharField(
        max_length=200,
        blank=True,
        help_text="Comma seperated keywords",
        error_messages={
            "required": errcode.topicourseTagInvalid,
            "invalid": errcode.topicourseTagInvalid,
            })
    topicourseType = models.CharField(
        max_length=200,
        blank=True,
        error_messages={
            "required": errcode.topicourseTypeInvalid,
            "invalid": errcode.topicourseTypeInvalid,
            })
    topicourseLevel = models.SmallIntegerField(
        max_length=1,
        choices=LEVELS,
        null=True,
        error_messages={
            "invalid": errcode.topicourseLevelInvalid,
            "invalid_choice": errcode.topicourseLevelInvalid,
            })

# put all vote into this table
class UserReview(Document):
    reviewedSubjectID = ObjectIdField()
    reviewedSubjectType = StringField() #topicourse, topiquiz, discussion
    reviewCreatorUserID = ObjectIdField()
    reviewVote = IntField()
    reviewContent = StringField()

class TopicoursesReview(EmbeddedDocument):
    topicoursesReviewCreatedTimeStamp = DateTimeField(default=datetime.datetime.now)
    topicoursesReviewCreatorUserID = ObjectIdField()
    topicoursesReviewContent = StringField()

class Topiquiz(EmbeddedDocument):
    #Todo: is this necessary?
    topiquizId = ObjectIdField(primary_key=True)
    topiquizType = IntField()
    topiquizQuestion = StringField()
    topiquizOption = ListField(StringField())
    topiquizAnswer = StringField()
    topiquizExplanation = StringField()
    #Todo this should not change when being edited
    topiquizCreatedTimeStamp = DateTimeField(default=datetime.datetime.now)
    topiquizCreatorUserID = LongField(required=True)
    topiquizErrorFlag = BooleanField()
    topiquizErrorFlagUserID = ObjectIdField()
    topiquizErrorFlagTimeStamp = DateTimeField()
    #Topiquiz active or not
    topiquizState = BooleanField()

class Topicourses(Document):
    topicourseId = ObjectIdField(primary_key=True)
    #Todo this should not change when being edited
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

