import json
from django.http import HttpResponse
# Create your views here.

def get_tuition_map(func):
    def new_view(request, *karg, **kwargs):
        # get user_emai
        raw_data = func('test@test.com')
        #format json output
        return HttpResponse(json.dumps(raw_data, sort_keys=True, indent=4))
    return new_view

@get_tuition_map
def get_user_appointment(user_email):
    userAppointments = {}

    userAppointments['UserAppointmentsList']=[]
    for i in range(0,2):
        userAppointment={}
        userAppointment['userAppointmentDate']=121113
        userAppointment['userAppointmentStartTime']=1200+i*100
        userAppointment['userAppointmentTitle']='test appointment title'
        userAppointment['userAppointmentCost']=20+i*10
        userAppointment['userAppointmentTutorMessage']='appointment tutor message'

        userAppointments['UserAppointmentsList'].append(userAppointment)

    return userAppointments

@get_tuition_map
def get_user_request(user_email):
    userRequests={}

    userRequests['userRequestsList']=[]
    for i in range(0,2):
        userRequest={}
        userRequest['userRequestStudentName']='test studentName'
        userRequest['userRequestTutorName']='test tutorName'
        userRequest['userRequestTuitionLevel']='college'
        userRequest['userRequestTuitionSubject']='maths'
        userRequest['userRequestTuitionLearningGoal']='test learningGoal'
        userRequest['userRequestTimeZone']=1+i
        userRequest['userRequestTimePreference']='test timePreference'
        userRequest['userRequestDatePreference']='test datePreference'
        userRequest['userRequestOther']='test requestOther'

        userRequests['userRequestsList'].append(userRequest)

    return userRequests

@get_tuition_map
def get_tutor_reply(user_email):
    tutorReplys={}

    tutorReplys['tutorReplysList']=[]
    for i in range(0,2):
        tutorReply={}
        tutorReply['tutorReplyRequestID']=777+i*111
        tutorReply['tutorReplyPriceQuote']=20
        tutorReply['tutorReplyTimeZone']=8
        tutorReply['tutorReplyMessage']='test tutorReplyMessage'
        tutorReply['tutorReplyTimeSlotList']=[]
        for j in range(0,3):
            tutorReplyTimeSlot=12+j
            tutorReply['tutorReplyTimeSlotList'].append(tutorReplyTimeSlot)

        tutorReplys['tutorReplysList'].append(tutorReply)

    return tutorReplys

