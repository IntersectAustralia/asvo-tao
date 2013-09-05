"""
==================
tao.settings
==================

Common Django settings
"""
import sys
from os.path import abspath, dirname, join, split

# Django settings for tao project.

DEBUG = False

PROJECT_PATH = abspath(split(__file__)[0])
PROJECT_DIR = dirname(PROJECT_PATH)

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Australia/Melbourne'
USE_TZ=True

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-au'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
import os
STATIC_ROOT = os.path.join(os.path.dirname(__file__), '..', 'static')


# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # os.path.join(os.path.dirname(__file__), '../../docs/', 'build'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'g070@k2w3k1l&&804i+(+dj9++-rbojrd*&w3l97#ofkpyyl!-'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'tao.shibboleth.ShibbolethUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'activitylog.middleware.ActivityLogMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "tao.context_processors.add_tab_to_context",
)

from django.contrib import messages
# to match twitter bootstrap's css tags
MESSAGE_TAGS = {
    messages.DEBUG: 'debug',  # not used so don't bother customising
    messages.INFO: 'alert alert-info',
    messages.SUCCESS: 'alert alert-success',
    messages.WARNING: 'alert',  # warning styling is the default
    messages.ERROR: 'alert alert-error',
}

ROOT_URLCONF = 'tao.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(__file__), "templates"),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'south',
    'tao',
    'captcha',
    'django_rules',
    'django_extensions',
    'tastypie',
    'activitylog',
    'tap',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(os.path.dirname(__file__), 'django.log'),
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'tao': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
        'django.request': {
            'handlers': ['console', 'file'],
            'level': 'WARNING',
            'propagate': True,
        }
    }
}

from django.core.urlresolvers import reverse_lazy
LOGIN_REDIRECT_URL = reverse_lazy('tao.views.home')
LOGIN_URL = reverse_lazy('tao.views.login')

## AUTH_PROFILE_MODULE = 'tao.UserProfile'  # appname.modelname
AUTH_USER_MODEL = 'tao.TaoUser'

EMAIL_HOST = 'gpo.swin.edu.au'
EMAIL_PORT = '25'

EMAIL_ACCEPT_SUBJECT = 'Welcome to ASVO TAO'
EMAIL_REJECT_SUBJECT = 'Your request for access to ASVO TAO has been rejected'
EMAIL_FROM_ADDRESS = 'admin@asvo.org.au'

RECAPTCHA_PUBLIC_KEY = '6Le-6tUSAAAAANY2atxpkcNZyPcLQSM7n2Lf8rUT'
RECAPTCHA_PRIVATE_KEY = '6Le-6tUSAAAAAPKhcTQI_Ecjff3Vw1Jn0Iu7u3kE'
RECAPTCHA_USE_SSL = True

NUM_RECORDS_PER_PAGE = 10

FILES_BASE = '/tmp/'  # please include a trailing slash

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'django_rules.backends.ObjectPermissionBackend',
    'tao.shibboleth.ShibbolethUserBackend',
)

MAX_DOWNLOAD_SIZE = 512 * 2**20

API_ALLOWED_IPS = (
                   '127.0.0.1',
                   )

INITIAL_JOB_STATUS = 'HELD'
INITIAL_JOB_MESSAGE = "Your job has been %s successfully, you will receive an e-mail notifying you when it has been completed."

#
# To avoid changing the directory structure until after we have confirmed
# the repository structure and replacing buildout with pip,
# set up the path and installed apps for the UI modules
#
UI_DIR = join(dirname(PROJECT_DIR), 'ui')

# The order of the tuples here determines the order that the tabs are listed
# in the UI
MODULES_PATHS = (
    ('job_type', 'job_type'),
    ('light_cone', 'light-cone'),
    ('sed', 'sed'),
    # ('telescope', 'telescope'),
    ('mock_image', 'mock_image'),
)
sys.path.extend([join(UI_DIR, module[1]) for module in MODULES_PATHS])
INSTALLED_APPS += tuple(['taoui_' + module[0] for module in MODULES_PATHS])
MODULES = tuple([module[0] for module in MODULES_PATHS])
#INSTALLED_APPS += tuple(('taoui_' + module_name for module_name in MODULES))


# This is the 'tab-id' the module occupies in the interface
MODULE_INDICES = {
                  'job_type': '1',
                  'light_cone': '2',
                  'sed': '3',
                  'mock_image': '4',
                  'record_filter': '5',
                  'output_format': '6',
                  'summary': '7',
                  'telescope': '8'
                  }

TAO_VERSION = '0.28.2'

AAF_DS_URL = 'https://ds.test.aaf.edu.au/discovery/DS'
AAF_APP_ID = 'https://example.intersect.org.au/shibboleth'
AAF_SESSION_URL = 'https://example.intersect.org.au/Shibboleth.sso/Login'
AAF_LOGOUT_URL = 'https://example.intersect.org.au/Shibboleth.sso/Logout'

AAF_USERNAME = 'SHIB_auEdupersonSharedToken'
AAF_FIRST_NAME = 'SHIB_givenName'
AAF_LAST_NAME = 'SHIB_surname'
AAF_EMAIL = 'SHIB_email'
AAF_COOKIE_PREFIX = '_shibsession_'

STATIC_URL = '/static/'
FILES_BASE = '/tmp/'  # please include a trailing slash

# EMAIL_HOST = 'localhost'
# EMAIL_PORT = '25'

EMAIL_FROM_ADDRESS = 'admin@localhost'

API_ALLOWED_IPS = (
                   '127.0.0.1'
                   )

ALLOWED_HOSTS = ['localhost', '127.0.0.1']
USE_CAPTCHA=True

#
# Activity Log settings
#
#Ignore responses altogether?
ACTIVITYLOG_LOG_RESPONSE=False
#Should we log full HTML responses?
ACTIVITYLOG_LOG_HTML_RESPONSE = False
# If we how do we recognized a full HTML response 
ACTIVITYLOG_HTML_START = "<!DOCTYPE html"

#
# Pretty print the metadata being passed to the browser?
# Useful for debugging, but much larger payload
#
METADATA_PRETTY_PRINT = DEBUG
