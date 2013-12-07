# Create your views here.

# [] is list
# {} is dictionary
def getUserTopicourses(user_email, get_type, num):
    topicourses = {}

    topicourses['userTopicoursesList'] = []
    for j in range(0, 3):
        topicourse = {}
        topicourse['userTopicoursesTimeStamp'] = 0
        topicourse['topicourseCreatorUserID'] = 10000
        topicourse['topicourseTitle'] = 'topicourseTitleForTest'
        topicourse['topicoursePath'] = '/redirect/url/'

        topicourse['userTopiquizList'] = []
        for i in range(0, 3):
            topiquiz = {}
            topiquiz['userTopiquizTimeStamp'] = i
            topiquiz['userTopiquizResults'] = 80 + i
            topicourse['userTopiquizList'].append(topiquiz)

        topicourses['userTopicoursesList'].append(topicourse)


    return topicourses

def getUserTopiquestions(user_email, get_type, num):
    topiquestions = {}

    topiquestions['userTopiquestionsList'] = []
    for j in range(0, 3):
        topiquestion = {}
        topiquestion['userTopiquestionTimeStamp'] = 0
        topiquestion['topiquestionCreatorUserID'] = 10000
        topiquestion['topiquestionTitle'] = 'topiquestionTitleForTest'
        topiquestion['topiquestionPath'] = '/redirect/url/'

        topiquestions['userTopiquestionsList'].append(topiquestion)

    return topiquestions
