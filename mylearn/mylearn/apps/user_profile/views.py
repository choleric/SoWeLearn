from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from forms import UserProfileForm, TutorProfileForm
from models import UserPersonalProfile

from mylearn.apps import errcode
from mylearn.apps import JsonResponse
from mylearn.apps.baseviews import UserRelatedFormView
# Create your views here.

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
        educationCredential['userEducationInfo']='test education info'
        educationCredential['IsVerified']=True
        educationCredential['verifiedTimeStamp']=11110+i
        educationCredential['verifiedStaffId']=11
        personalProfile['userEducationCredential'].append(educationCredential)
    personalProfile['userWorkCredential']=[]
    for i in range(0,2):
        workCredential={}
        workCredential['userWorkInfo']='test work info'
        workCredential['IsVerified']=True
        workCredential['verifiedTimeStamp']=22220+i
        workCredential['verifiedStaffId']=22
        personalProfile['userWorkCredential'].append(workCredential)
    userProfile['personalProfile']=personalProfile
    userProfile['userLocation']="test location"
    userProfile['tutorTuitionTopics']="chemical engineering"
    userProfile['tutorTuitionAverageHourlyRateMiddleSchool']=20
    userProfile['tutorTuitionAverageHourlyRateHighSchool']=30
    userProfile['tutorTuitionAverageHourlyRateCollege']=0

    return userProfile

def profile2(request):
    userProfile = getUserProfile('test@test.com')
    return JsonResponse(errcode.SUCCESS, userProfile)

def getUserTopicourses(userID,type,number):
    userTopicoursesList = []
    for i in range(0,2):
        userTopicourse={}
        userTopicourse['userTopicoursesTimestamp']=1234+i
        userTopicourse['userTopicourseCreatorUserID'] = 0
        userTopicourse['topicourseTitle'] = 'test topic title'
        userTopicourse['topicoursePath'] = 'test path'
        userTopicourse['userTopicquizList']=[]
        for j in range(0,3):
            userTopicquiz={}
            userTopicquiz['userTopicquizTimestamp']=9876+j
            userTopicquiz['userTopicquizResult']='2013-14-25'
            userTopicourse['userTopicquizList'].append(userTopicquiz)
        userTopicoursesList.append(userTopicourse)

    return  userTopicoursesList

def topicourses(request):
    userTopicourses = getUserTopicourses("1146","teaching","2")
    return JsonResponse(errcode.SUCCESS, userTopicourses)

class ProfileView(UserRelatedFormView) :
    form_class = UserProfileForm

    def get(self, request, *args, **kwargs):
        user_profile = UserPersonalProfile.objects.get(userID = request.user.pk)
        if user_profile.verifiedTutor:
            self.form_class = TutorProfileForm
        return super(ProfileView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user_profile = UserPersonalProfile.objects.get(userID = request.user.pk)
        if user_profile.verifiedTutor:
            self.form_class = TutorProfileForm
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if not form.is_valid():
            err = errcode.profileUnknown
            for field, v in form.errors.iteritems() :
                if 1 > len(v) :
                    continue
                err = v[0]
                break

            return HttpResponse(err)

        form.instance.userID = request.user.pk
        form.save()
        return JsonResponse(errcode.SUCCESS)


profile = ProfileView.as_view()
