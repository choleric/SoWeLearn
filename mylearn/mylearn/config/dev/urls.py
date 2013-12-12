"""
development url configuration
"""
import os
import os.path

from settings import BASE_DIR


__staticDir = os.path.join(BASE_DIR, os.pardir, "static")
__htmlDir = os.path.join(__staticDir, "html")
__cssDir = os.path.join(__staticDir, "css")
__jsDir = os.path.join(__staticDir, "js")
__imgDir = os.path.join(__staticDir, "images")

urlpatterns += patterns('',
    (r'^html/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': __htmlDir}),
    (r'^css/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': __cssDir}),
    (r'^js/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': __jsDir}),
    (r'^images/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': __imgDir}),
)
