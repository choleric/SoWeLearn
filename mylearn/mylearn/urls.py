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
    url(r'^modify-user-quote/', 'modify_user_quote'),
    url(r'^modify_work_and_education_credential/','modify_work_and_education_credential'),
    url(r'^modify_work_and_education_credential/','modify_work_and_education_credential'),
)

urlpatterns += patterns(PROJECT_APP_PREFIX + '.topicourse.views',
    url(r'^userTopicourses/', 'userTopicourses'),
    url(r'^userTopiquestions/', 'userTopiquestions'),
)

urlpatterns += patterns(PROJECT_APP_PREFIX + '.tuition_map.views',
    url(r'^getUserAppointment/', 'get_user_appointment'),
    url(r'^getUserRequest/', 'get_user_request'),
    url(r'^getTutorReply/', 'get_tutor_reply'),
)

# Load extra urls config file
__extraURLConfigFile = os.path.join(PROJECT_CONFIG_DIR, "urls.py")
if os.path.exists(__extraURLConfigFile) :
    execfile(__extraURLConfigFile)
