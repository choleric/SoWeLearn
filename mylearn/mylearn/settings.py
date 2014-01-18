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

def get_project_app_qulified_name(app) :
    return "%s.%s"%(PROJECT_APP_PREFIX, app)

# Application definition
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
     'django.contrib.comments',
    'mongodbforms',
    'django_youtube',
    'fluent_comments',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    PROJECT_APP_PREFIX + '.general.middleware.ProcessAjaxRedirectMiddleware',
)

ROOT_URLCONF = PROJECT_NAME + ".urls"
WSGI_APPLICATION = PROJECT_NAME + '.wsgi.application'

#CSRF Settings
CSRF_COOKIE_NAME = "_t"

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

# auth settings
TEMPLATE_CONTEXT_PROCESSORS = (
    # Required by allauth template tags
    "django.core.context_processors.request",
    'django.contrib.auth.context_processors.auth',
    # allauth specific context processors
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

STATIC_URL = '/static/'
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'
LOGOUT_URL = '/accounts/logout/'
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SESSION_COOKIE_HTTPONLY = False
SESSION_COOKIE_NAME = "_l"
SESSION_COOKIE_AGE = 600 # default cookie max-age 10 minutes
ANONYMOUS_USER_ID = -1
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "http"
# allauth settings
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION= "mandatory"
SOCIALACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_PASSWORD_MIN_LENGTH = 6
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_LOGOUT_REDIRECT_URL = "/"
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_SIGNUP_FORM_CLASS = get_project_app_qulified_name('allauth_override_template.forms.SignupFormAdd')

SOCIALACCOUNT_PROVIDERS = \
    {
    #Settings for Facebook
    'facebook':
       {'SCOPE': ['email', 'publish_stream'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'METHOD': 'oauth2',
        'LOCALE_FUNC': lambda request: 'en_US', #what should this be referred to?
        'VERIFIED_EMAIL': True},
    #Settings for Google
    'google':
        { 'SCOPE': ['https://www.googleapis.com/auth/userinfo.profile'],
          'AUTH_PARAMS': { 'access_type': 'online' } },
    #Settings for Linkedin
    'linkedin':
      {'SCOPE': ['r_emailaddress'],
       'PROFILE_FIELDS': ['id','first-name','last-name','email-address','picture-url','public-profile-url']}
    }

#Settings for django-youtube

YOUTUBE_AUTH_EMAIL = 'SoWeLearn.com@gmail.com'
YOUTUBE_AUTH_PASSWORD = '140101swl'
YOUTUBE_DEVELOPER_KEY = 'AI39si5hjixvG_TbDOrLbNQ534Zo-DzIeP2EzLGFcsIKoaHGosm018jiN5fLPZE-13-lJtkEPBb8HH5DWFTolrdtQI_jWAiu_g'
YOUTUBE_CLIENT_ID = '525773080463.apps.googleusercontent.com'

# url to redirect after upload finishes, default is respected `video` page
YOUTUBE_UPLOAD_REDIRECT_URL = '/youtube/videos/'

# url to redirect after deletion video, default is `upload page`
YOUTUBE_DELETE_REDIRECT_URL = '/youtube/delete/'

COMMENTS_APP = 'fluent_comments'

# fluent-comments settings:
FLUENT_COMMENTS_USE_EMAIL_MODERATION = True
FLUENT_COMMENTS_MODERATE_AFTER_DAYS = 14
FLUENT_COMMENTS_CLOSE_AFTER_DAYS = 60
FLUENT_COMMENTS_AKISMET_ACTION = 'moderate'
AKISMET_API_KEY = None  # Add your Akismet key here to enable Akismet support
AKISMET_IS_TEST = True  # for development/example apps.
FLUENT_COMMENTS_USE_EMAIL_NOTIFICATION = False

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
            INSTALLED_APPS += (get_project_app_qulified_name(app), )

INSTALLED_APPS += (
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # include the providers for all auth:
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.linkedin',
    'allauth.socialaccount.providers.twitter',
)
# IMPORTANT no configuration below is allowed
