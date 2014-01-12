from forms import UserProfileForm, TutorProfileForm, UserEducationForm, UserWorkForm
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

class ProfileViewIntegrated(UserRelatedFormView):
    form_class = UserProfileForm

    def get_form_parent_document(self, request, parent_document):
        kwargs = super(ProfileViewIntegrated, self).get_form_kwargs()
        kwargs.update(
            {'parent_document': parent_document}
        )
        if 'position' in request.POST:
            position = int(request.POST['position'])
            del request.POST['position']
            kwargs.update(
                {'position': position,
                 'data': request.POST}
            )
        return kwargs

    def get(self, request, *args, **kwargs):
        user_profile = UserPersonalProfile.objects.get(userID = request.user.pk)
        include_fields = ['userSkypeID', 'aboutUserQuote', 'userLocation',
                           'userEducationInfo', 'userWorkInfo', 'IsVerified']
        data = self.from_object_to_dict(user_profile, include_fields)
        return JsonResponse(code = errcode.SUCCESS, data = data, isHTMLEncode = False)

    def post(self, request, *args, **kwargs):
        if 'userEducationInfo' in request.POST:
            self.form_class = UserEducationForm
            form_class = self.get_form_class()
            user_profile = UserPersonalProfile.objects.get(userID = request.user.pk)
            # validate the data for list
            if self.pre_validation_for_list(request, 10, user_profile, 'userEducationCredential'):
                return JsonResponse(errcode.ListMaxLengthExceeded)

            form = form_class(**self.get_form_parent_document(request, user_profile))
            if not form.is_valid():
                return JsonResponse(errcode.profileEduInvalid)

        elif 'userWorkInfo' in request.POST:
            self.form_class = UserWorkForm
            form_class = self.get_form_class()

            user_profile = UserPersonalProfile.objects.get(userID = request.user.pk)
            self.pre_validation_for_list(request, 10, user_profile, 'userWorkCredential')

            form = form_class(**self.get_form_parent_document(request, user_profile))
            if not form.is_valid():
                return JsonResponse(errcode.profileWorkInvalid)


        else:
            form_class = self.get_form_class()
            form = self.get_form(form_class)

            if not form.is_valid():
                err = errcode.TutorProfileUnknown
                for field, v in form.errors.iteritems() :
                    if 1 > len(v) :
                        continue
                    err = form.Meta.err_maps[field]
                    break

                return JsonResponse(err)
            form.instance.userID = request.user.pk

        form.save()
        return JsonResponse(errcode.SUCCESS)


personalProfile = ProfileViewIntegrated.as_view()

class TutorProfileView(UserRelatedFormView):
    form_class = TutorProfileForm

    def get(self,request, *args, **kwargs):
        user_profile = UserPersonalProfile.objects.get(userID = request.user.pk)
        if not user_profile.verifiedTutor:
            return JsonResponse(errcode.UserNotVerifiedAsTutor)
        return super(TutorProfileView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if not form.is_valid():
            err = errcode.TutorProfileUnknown
            for field, v in form.errors.iteritems() :
                if 1 > len(v) :
                    continue
                err = form.Meta.err_maps[field]
                break

            return JsonResponse(err)

        form.instance.userID = request.user.pk
        form.save()
        return JsonResponse(errcode.SUCCESS)

tutorProfile = TutorProfileView.as_view()
