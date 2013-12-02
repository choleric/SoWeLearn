from mongoengine import *
from django.db import models

# Create your models here.

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

