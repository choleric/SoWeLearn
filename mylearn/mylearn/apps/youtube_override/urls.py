from django.conf.urls import url, patterns
from ...settings import PROJECT_APP_PREFIX

urlpatterns = patterns('django_youtube.views',
    # list of the videos
    url(r'^videos/?$', 'video_list', name="youtube_video_list"),

    # video  display page, convenient to use in an iframe
    url(r'^video/(?P<video_id>[\w.@+-]+)/$', 'video', name="youtube_video"),

    # upload page with a form
    url(r'^direct-upload/?$', 'direct_upload', name="youtube_direct_upload"),

    # remove video, redirects to upload page when it's done
    url(r'^video/remove/(?P<video_id>[\w.@+-]+)/$', 'remove', name="youtube_video_remove"),
)

urlpatterns += patterns(PROJECT_APP_PREFIX + '.youtube_override.views',
    # upload video meta information
    url(r'^upload/?$', 'upload_meta', name="youtube_upload_meta"),

    # page that youtube redirects after upload
    url(r'^upload/return/?$', 'upload_return', name="youtube_upload_return"),
)