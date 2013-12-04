import json
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

def getUserProfile(user_email):
    userProfile= {}
    userProfile['userName']='test name'
    userProfile['userEmail']=user_email
    userProfile['userSkypeID']='testSkypeID'

    personalProfile={}
    personalProfile['aboutUserQuote']='Test About Me'
    personalProfile['userEducationCredential']=[]
    for i in range(0,2):
        educationCredential={}
        educationCredential['educationInfo']='test education info'
        educationCredential['IsVerified']=True
        educationCredential['verifiedTimeStamp']=11110+i
        educationCredential['verifiedStaffID']=11
        personalProfile['userEducationCredential'].append(educationCredential)
    personalProfile['userWorkCredential']=[]
    for i in range(0,2):
        workCredential={}
        workCredential['workInfo']='test wrok info'
        workCredential['IsVerified']=True
        workCredential['verifiedTimeStamp']=22220+i
        workCredential['verifiedStaffID']=22
        personalProfile['userWorkCredential'].append(workCredential)
    userProfile['personalProfile']=personalProfile
    userProfile['userLocation']="test location"
    userProfile['tutorTuitionTopics']="chemical engineering"
    userProfile['tutorTuitionAverageHourlyRateMiddleSchool']=20
    userProfile['tutorTuitionAverageHourlyRateHighSchool']=30
    userProfile['tutorTuitionAverageHourlyRateCollege']=0
    return userProfile
userProfile = getUserProfile('test@test.com')
print json.dumps(userProfile)