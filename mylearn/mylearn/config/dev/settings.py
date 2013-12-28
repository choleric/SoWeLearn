"""
This is django setting.py for development
"""
import os
import logging

__log = logging.getLogger(__name__)

DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []
DBNAME = 'mylearn'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '.sqlite3.tmp')
    },
    'mongodb' : {
      'ENGINE' : 'django_mongodb_engine',
      'NAME' : DBNAME
    }
}

# for tests
INSTALLED_APPS += (
    #To test allauth
    'django.contrib.admin',
)

# for allauth requiring site_id
SITE_ID = u"8fe7aa759e654e2662000000"

#EMAIL BACKEND FOR DJANGO-ALLAUTH
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
