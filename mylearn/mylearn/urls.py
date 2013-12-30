import os.path

from django.conf.urls import patterns
from django.conf.urls import url
from django.conf.urls import include
from settings import PROJECT_APP_PREFIX, get_project_app_qulified_name
from settings import PROJECT_CONFIG_DIR
#To test allauth
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(PROJECT_APP_PREFIX + '.user_profile.views',
    url(r'^$', 'welcome'),
    url(r'^test/', 'test'),
    url(r'^register/', 'register_'),
    url(r'^login/', 'login'),
    url(r'^profile/', 'profile', name="profile_url"),
    url(r'^topicourses/', 'topicourses'),#test topicourses -zhouwei
    url(r'^modify-user-quote/', 'modify_user_quote'),
    url(r'^modify_work_and_education_credential/','modify_work_and_education_credential'),
    url(r'^modify_work_and_education_credential/','modify_work_and_education_credential'),
)

urlpatterns += patterns(PROJECT_APP_PREFIX + '.topicourse.views',
    url(r'^userTopicourses/', 'user_topicourses'),
    url(r'^userTopiquestions/', 'user_topiquestions'),
)

urlpatterns += patterns(PROJECT_APP_PREFIX + '.tuition_map.views',
    url(r'^getUserAppointment/', 'get_user_appointment'),
    url(r'^getUserRequest/', 'get_user_request'),
    url(r'^getTutorReply/', 'get_tutor_reply'),
)

urlpatterns += patterns('',
    (r'^accounts/', include(get_project_app_qulified_name('allauth_override_template.urls'))),
    (r'^accounts/social/', include(get_project_app_qulified_name('allauth_socialaccount.urls'))),
    (r'^accounts/', include('allauth.urls')),
)

#To test allauth
urlpatterns += patterns('',
    (r'^admin/', include(admin.site.urls)),
)
# Load extra urls config file
__extraURLConfigFile = os.path.join(PROJECT_CONFIG_DIR, "urls.py")
if os.path.exists(__extraURLConfigFile) :
    execfile(__extraURLConfigFile)
