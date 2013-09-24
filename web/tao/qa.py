"""
==================
tao.qa
==================

Settings for QA environment
"""
from tao.settings import *

DEBUG=True
TEMPLATE_DEBUG=DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'tao',                      # Or path to database file if using sqlite3.
        'USER': 'tao',                      # Not used with sqlite3.
        'PASSWORD': 'tao',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

STATIC_CTX = '/tao'
STATIC_URL = '/tao/static/'

EMAIL_HOST = 'localhost'
EMAIL_PORT= '25'

AAF_DS_URL = 'https://ds.test.aaf.edu.au/discovery/DS'
AAF_APP_ID = 'https://asvo-qa.intersect.org.au/shibboleth'
AAF_SESSION_URL = 'https://asvo-qa.intersect.org.au/Shibboleth.sso/Login'
AAF_LOGOUT_URL = 'https://asvo-qa.intersect.org.au/Shibboleth.sso/Logout'

TRACKING_ID='UA-999999-99'
