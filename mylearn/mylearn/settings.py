"""
Django settings for mylearn project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
import os.path
import logging
import logging.config
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Find project name
PROJECT_NAME = "mylearn"
PROJECT_DIR = os.path.join(BASE_DIR, PROJECT_NAME)


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'qukye=pnq%+(4o571gq=#*nur+noruonh=ulci3^8df!%4e3ac'


# Application definition
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = PROJECT_NAME + '.urls'

WSGI_APPLICATION = PROJECT_NAME + '.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOCALE_PATHS = (
    os.path.join(PROJECT_DIR, "locale"),
)


# Load settings.py(development or production) file based on os environment variable "MYLEARN_MODE", default production mode
__MODE_DEV= "dev"
__MODE_PRODUCTION = "production"
__mode = __MODE_PRODUCTION
__mode_key = "MYLEARN_MODE"

if __mode_key in os.environ :
    __mode_tmp = os.environ[__mode_key].strip()
    if 1 > len(__mode_tmp) or (__mode_tmp != __MODE_DEV and __mode_tmp != __MODE_PRODUCTION) :
        pass
    else :
        __mode = __mode_tmp
# Log config
__logConfigFile = os.path.join(PROJECT_DIR, "config", __mode, "log.conf")
if not os.path.exists(__logConfigFile) :
    print "Log config file not found......."
    sys.exit(1)

logging.config.fileConfig(__logConfigFile)


# Do the load operation
__settingFile = os.path.join(PROJECT_DIR, "config", __mode, "settings.py")
if not os.path.exists(__settingFile) :
    logging.getLogger(__name__).error("setting file '%s' not found", __settingFile)
    sys.exit(1)

execfile(__settingFile)


# IMPORTANT no configuration below is allowed
