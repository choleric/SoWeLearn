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
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # include the providers for all auth:
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.linkedin',
    'allauth.socialaccount.providers.twitter',
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

# auth settings
TEMPLATE_CONTEXT_PROCESSORS = (
    # Required by allauth template tags
    "django.core.context_processors.request",
    'django.contrib.auth.context_processors.auth',
    # allauth specific context processors
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
)

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

LOGIN_REDIRECT_URL = '/accounts/%(username)s/'
LOGIN_URL = '/accounts/signin/'
LOGOUT_URL = '/accounts/signout/'
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_NAME = "_l"
SESSION_EXPIRE_AT_BROWSER_CLOSE =True
ANONYMOUS_USER_ID=-1

# allauth settings
ACCOUNT_ADAPTER = "allauth.account.adapter.DefaultAccountAdapter" #can be customized
ACCOUNT_AUTHENTICATION_METHOD="email"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS=1
ACCOUNT_EMAIL_REQUIRED=True
ACCOUNT_EMAIL_VERIFICATION= "mandatory"
ACCOUNT_USERNAME_REQUIRED=False
ACCOUNT_SIGNUP_FORM_CLASS = 'apps.allauth_override_template.forms.SignupFormAdd'
  #Specifies the adapter class to use, allowing you to alter certain default behaviour.
SOCIALACCOUNT_ADAPTER="allauth.socialaccount.adapter.DefaultSocialAccountAdapter"

SOCIALACCOUNT_PROVIDERS = \
    {
    #Settings for Facebook
    'facebook':
       {'SCOPE': ['email', 'publish_stream'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'METHOD': 'oauth2',
        'LOCALE_FUNC': 'path.to.callable', #what should this be referred to?
        'VERIFIED_EMAIL': True},
    #Settings for Google
    'google':
        { 'SCOPE': ['https://www.googleapis.com/auth/userinfo.profile'],
          'AUTH_PARAMS': { 'access_type': 'online' } }
    }

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

# IMPORTANT no configuration below is allowed
