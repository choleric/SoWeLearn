from django.http import HttpResponse
import json

from mylearn.apps import errcode
from mylearn.apps import JsonResponse
from mylearn.apps.baseviews import UserRelatedFormView, LoginRequriedView

from .models import QuizType
from .forms import TopicourseInfoForm, TopiquizTorFForm
# Create your views here.

# [] is list
# {} is dictionary
def getUserTopicourses(user_email, get_type, num):
    topicourses = {}

    topicourses['userTopicoursesList'] = []
    for j in range(0, 3):
        topicourse = {}
        topicourse['userTopicoursesTimeStamp'] = j
        topicourse['topicourseCreatorUserID'] = 10000
        topicourse['topicourseTitle'] = 'topicourseTitleForTest'
        topicourse['topicoursePath'] = '/redirect/url/'

        topicourse['userTopiquizList'] = []
        for i in range(0, 2):
            topiquiz = {}
            topiquiz['userTopiquizTimeStamp'] = i
            topiquiz['userTopiquizResults'] = 80 + i
            topicourse['userTopiquizList'].append(topiquiz)

        topicourses['userTopicoursesList'].append(topicourse)
    #sorted(topicourses.['userTopicoursesList'],key=topicourses.['userTopicoursesList'].)
    return topicourses

def user_topicourses(request):
    userTopicourses = getUserTopicourses('test@test.com','learning',3)
    userTopicourses = json.dumps(userTopicourses)
    return HttpResponse(userTopicourses)

def getUserTopiquestions(user_email, get_type, num):
    topiquestions = {}

    topiquestions['userTopiquestionsList'] = []
    for j in range(0, 3):
        topiquestion = {}
        topiquestion['userTopiquestionTimeStamp'] = j
        topiquestion['topiquestionCreatorUserID'] = 10000
        topiquestion['topiquestionTitle'] = 'topiquestionTitleForTest'
        topiquestion['topiquestionPath'] = '/redirect/url/'

        topiquestions['userTopiquestionsList'].append(topiquestion)

    return topiquestions

def user_topiquestions(request):
    userTopiquestions = getUserTopiquestions('test@test.com','learning',3)
    userTopiquestions = json.dumps(userTopiquestions)
    return HttpResponse(userTopiquestions)

class TopicourseFormView(UserRelatedFormView):
    form_class = TopicourseInfoForm

    def get(self, request):
        pass

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if not form.is_valid():
            err = errcode.profileUnknown
            for field, v in form.errors.iteritems() :
                if 1 > len(v) :
                    continue
                err = v[0]
                break

            return JsonResponse(err)

        form.instance.topicourseCreatorUserID = request.user.pk
        form.instance.topicourseID = request.POST['topicourseID']
        form.save()
        return JsonResponse(errcode.SUCCESS)

topicourse = TopicourseFormView.as_view()

def create_topicourse(request, topicourseID):
    HttpResponse("this should be set to html page for creating a topicourse with"
                 "topicourse id: %s" %topicourseID)

class TopiquizFormView(UserRelatedFormView):

    def select_form_class(self, request):
        if "topiquizType" in request.POST:
            quiz_type = int(request.POST["topiquizType"])
            if quiz_type==QuizType.TorF:
                self.form_class = TopiquizTorFForm
            else:
                return JsonResponse(errcode.topiquizTypeInvalid)
            return self.form_class
        else:
            return JsonResponse(errcode.topiquizTypeEmpty)

    def post(self, request, *args, **kwargs):
        self.select_form_class(request)
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        print form.is_valid()

        if not form.is_valid():
            err = errcode.profileUnknown
            for field, v in form.errors.iteritems() :
                if 1 > len(v) :
                    continue
                err = v[0]
                break

            return JsonResponse(err)

        form.instance.topiquizType = request.POST["topiquizType"]
        form.instance.topiquizCreatorID = request.user.pk

        form.save()
        return JsonResponse(errcode.SUCCESS)

topiquiz = TopiquizFormView.as_view()