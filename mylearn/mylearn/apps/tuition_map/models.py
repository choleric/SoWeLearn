from mongoengine import *
from django.db import models
import datetime

# Create your models here.

class UserAppointment(Document):
    #TO-DO
    STATUS_CHOICE = (
        ('F', 'Finished'),
        ('NF', 'Not Finished'),
    )
    userRequestStudentID = LongField()
    userRequestTutorID = LongField()

    #userAppointmentDate = DateTimeField()
    userAppointmentStartTime = DateTimeField()
    userAppointmentDuration = LongField()
    userAppointmentTitle = StringField()
    userAppointmentCost = IntField()
    userAppointmentTutorMessage = StringField()
    userAppointmentStatus = StringField(max_length=2, choices=STATUS_CHOICE)
    userAppointmentCreatedTimeStamp = DateTimeField(default=datetime.datetime.now)

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

