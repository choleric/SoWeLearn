from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.template import RequestContext
import json
import models
from .forms import UserQuoteForm, WorkAndEducationCredentialForm, LocationAndContactForm
from django.contrib.auth.decorators import login_required
from .. import code
from ..response import JsonResponse
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

def profile(request):
    userProfile = getUserProfile('test@test.com')

    #context = {'userProfile':userProfile}
    context = {'personalProfile': userProfile['personalProfile']}
    return render_to_response('userProfile.html',  context)

def profile2(request):
    userProfile = getUserProfile('test@test.com')
    return JsonResponse(code.SUCCESS, userProfile)

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
    return JsonResponse(code.SUCCESS, userTopicourses)

#user_db = models.User()

def test(request):
    return HttpResponse("hello world")

def welcome(request):
    return render_to_response('main.html')

def register_(request):
    if request.method == 'GET':
        return render_to_response('register.html', context_instance=RequestContext(request))
    else:

        user_email = request.POST.get('user_email')
        error = []

        if not user_db.get_user(user_email):
            context = {'user_info': request.POST}

            user_info = request.POST
            user_db.add_user(user_name=user_info.get('user_name'), user_email=user_info.get('user_email'),
                    user_location=user_info.get('user_location'))
            return render_to_response('welcome.html', context)
        else:
            error.append('%s already exists, please login' % user_email)
            context = {'errors': error}
            context.update(csrf(request))
            return render_to_response('welcome.html', context)
            #return HttpResponseRedirect('login.html')

def get_user_personal_profile(user_email):
    userProfile = models.UserPersonalProfile.objects(userEmail=user_email).first()

    return userProfile

def login(request):
    if request.method == 'GET':
        return render_to_response('login.html', context_instance=RequestContext(request))
    else:
        user_email= request.POST.get('user_email')

        #user=models.user.objects.get(user_email=user_email)
        user=models.user.objects.get(userEmail=user_email)
        userProfile = getUserProfile(user_email)

        if not user:
            context = { 'errors': '%s is not exist' % user_email}
        else:
            #context = {'user_info': user}
            context = {'userPersonalProfile': userProfile.userPersonalProfile}
        #return HttpResponseRedirect('welcome.html', context)
        return render_to_response('userProfile.html',  context)

def modify_user_quote(request):
    if request.POST:
        user_quote = UserQuoteForm(request.POST)
        if user_quote.is_valid() == True:
            #TODO
            #user.change_about_user_quote(user_quote['aboutUserQuote'])
            return HttpResponse(json.dumps({'success': True}))
        else:
            return HttpResponse(json.dumps({'success': False, 'errors': dict(user_quote.errors.items())}))

    else:
        raise Http404()


def modify_work_and_education_credential(request):
    if request.POST:
        workForm = WorkAndEducationCredentialForm(request.POST)
        if workForm.is_valid() == True:
            #TODO
            return HttpResponse(json.dumps({'success':True}))
        else:
            return HttpResponse(json.dumps({'success': False, 'errors': dict(workForm.errors.items())}))
    else:
        raise Http404()


def modify_location_and_contact_form(request):
    if request.POST:
        locationForm = LocationAndContactForm(request.POST)
        if locationForm.is_valid() == True:
            #TODO
            return HttpResponse(json.dumps({'success':True}))
        else:
            return HttpResponse(json.dumps({'success': False, 'errors': dict(locationForm.errors.items())}))
    else:
        raise Http404()

def edit_teaching_profile_form(request):
    """Function for update teaching profile."""
    if request.method == 'POST':
        teachingForm = forms.TeachingProfileForm(request.POST)
        if teachingForm.is_valid():
            newTeachingProfileForm = teachingForm.cleaned_data

            user = models.UserPersonalProfile.objects.get(userEmail='test@test.com') #To be replaced!
            if newTeachingProfileForm['tutorTuitionTopics']!='' :
                user.change_tutorTuitionTopics(newTeachingProfileForm['tutorTuitionTopics'])
            elif newTeachingProfileForm['tutorTuitionAverageHourlyRateMiddleSchool']!='':
                user.change_tutorTuitionAverageHourlyRateMiddleSchool(newTeachingProfileForm['tutorTuitionAverageHourlyRateMiddleSchool'])
            elif newTeachingProfileForm['tutorTuitionAverageHourlyRateHighSchool']!='':
                user.tutorTuitionAverageHourlyRateHighSchool(newTeachingProfileForm['tutorTuitionAverageHourlyRateHighSchool'])
            elif newTeachingProfileForm['tutorTuitionAverageHourlyRateCollege']!='':
                user.tutorTuitionAverageHourlyRateCollege(newTeachingProfileForm['tutorTuitionAverageHourlyRateCollege'])
            else:
                pass

            return HttpResponse(json.dumps({'success':True}))

        else:
            return HttpResponse(json.dumps({'success': False, 'errors': dict(teachingForm.errors.items())}))

    raise Http404()

