from django.http import HttpResponse
import json
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

def userTopicourses(request):
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

def userTopiquestions(request):
    userTopiquestions = getUserTopiquestions('test@test.com','learning',3)
    userTopiquestions = json.dumps(userTopiquestions)
    return HttpResponse(userTopiquestions)