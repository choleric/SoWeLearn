import os.path

from django.conf.urls import patterns
from django.conf.urls import url
from settings import PROJECT_APP_PREFIX
from settings import PROJECT_CONFIG_DIR

urlpatterns = patterns(PROJECT_APP_PREFIX + '.user_profile.views',
    url(r'^$', 'welcome'),
    url(r'^test/', 'test'),
    url(r'^register/', 'register_'),
    url(r'^login/', 'login'),
    url(r'^profile/', 'profile'),
    url(r'^profile2/', 'profile2'),
    url(r'^topicourses/', 'topicourses'),#test topicourses -zhouwei
)

urlpatterns += patterns(PROJECT_APP_PREFIX + '.topicourse.views',
    url(r'^userTopicourses/', 'userTopicourses'),
    url(r'^userTopiquestions/', 'userTopiquestions'),
)

urlpatterns += patterns(PROJECT_APP_PREFIX + '.tuition_map.views',
    url(r'^getUserAppointment/', 'get_tuition_map'),
    url(r'^getUserRequest/', 'get_tuition_map'),
    url(r'^getTutorReply/', 'get_tuition_map'),
)

# Load extra urls config file
__extraURLConfigFile = os.path.join(PROJECT_CONFIG_DIR, "urls.py")
if os.path.exists(__extraURLConfigFile) :
    execfile(__extraURLConfigFile)
