"""
This is django setting.py for development
"""
import os

DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '.sqlite3.tmp'),
    }
}
