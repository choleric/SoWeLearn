# Create your views here.
def getUserAppointment(user_email):
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

def getUserRequest(user_email):
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

def getTutorReply(user_email):
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

print getTutorReply('test_email')