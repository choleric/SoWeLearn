"""
Django settings for mylearn project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import sys
import os
import os.path
import logging
import logging.config
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Find project name
PROJECT_NAME = "mylearn"
PROJECT_APP_NAME = "apps"
PROJECT_APP_PREFIX = PROJECT_NAME + "." + PROJECT_APP_NAME
PROJECT_DIR = os.path.join(BASE_DIR, PROJECT_NAME)


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'qukye=pnq%+(4o571gq=#*nur+noruonh=ulci3^8df!%4e3ac'


# Application definition
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'userena',
    'guardian',
    'easy_thumbnails',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = PROJECT_NAME + ".urls"
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

# accounts setting
AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)
ANONYMOUS_USER_ID = -1
AUTH_PROFILE_MODULE = 'accounts.UserProfile'
LOGIN_REDIRECT_URL = '/accounts/%(username)s/'
LOGIN_URL = '/accounts/signin/'
LOGOUT_URL = '/accounts/signout/'


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

PROJECT_CONFIG_DIR = os.path.join(PROJECT_DIR, "config", __mode)
# Log config
__logConfigFile = os.path.join(PROJECT_CONFIG_DIR, "log.conf")
if not os.path.exists(__logConfigFile) :
    print "Log config file not found......."
    sys.exit(1)

logging.config.fileConfig(__logConfigFile)
__logger = logging.getLogger(__name__)


# Do the load operation
__settingFile = os.path.join(PROJECT_CONFIG_DIR, "settings.py")
if not os.path.exists(__settingFile) :
    __logger.error("setting file '%s' not found", __settingFile)
    sys.exit(1)

execfile(__settingFile)


# Automatically load apps from apps directory
__appsDir = os.path.join(PROJECT_DIR, PROJECT_APP_NAME)
if not os.path.exists(__appsDir) :
    __logger.error("apps directory '%s' not found", __appsDir)
    sys.exit(1)

__appList = os.listdir(__appsDir)
if None != __appList :
    for app in __appList :
        if os.path.isdir(os.path.join(__appsDir, app)) :
            __logger.info("load app: %s", app)
            INSTALLED_APPS += ("%s.%s"%(PROJECT_APP_PREFIX, app),)

# IMPORTANT no configuration below is allowed
