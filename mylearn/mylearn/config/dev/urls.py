"""
development url configuration
"""
import os
import os.path

from settings import BASE_DIR


__staticDir = os.path.join(BASE_DIR, os.pardir, "static")
__htmlDir = os.path.join(__staticDir, "html")

urlpatterns += patterns('',
    (r'^$', 'django.views.static.serve',
            {'document_root': __htmlDir, 'path': "main.html"}),
    (r'^(?P<path>[^.]+\.html)$', 'django.views.static.serve',
            {'document_root': __htmlDir}),
    (r'^(?P<path>.+?\.css)$', 'django.views.static.serve',
            {'document_root': __staticDir}),
    (r'^(?P<path>.+?\.js)$', 'django.views.static.serve',
            {'document_root': __staticDir}),
    (r'^(?P<path>[^.]+\.(png|jpg|jpeg|gif))$', 'django.views.static.serve',
            {'document_root': __staticDir}),
)
