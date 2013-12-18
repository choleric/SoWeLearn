"""
This is django setting.py for development
"""
import os
import logging

from mongoengine import connect
__log = logging.getLogger(__name__)

DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []

DBNAME = 'mylearn'
try :
    connect(DBNAME, host='localhost', port=27017)
except Exception as e :
    __log.error("mongodb connnect: %s", e)


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '.sqlite3.tmp'),
    }
}

# usernea settings
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'yourgmailaccount@gmail.com'
EMAIL_HOST_PASSWORD = 'yourgmailpassword'

# for tests
INSTALLED_APPS += (
    #To test allauth
    'django.contrib.admin',
)

# for allauth requiring site_id
SITE_ID = 1