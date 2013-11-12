"""
==================
tao.production
==================

Production settings. It uses a module not available open source that overrides DATABASES.
"""
from tao.settings import *

DEBUG=False
TEMPLATE_DEBUG=DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB, SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED'
        }
    }
}

# Set this variable in taosecrets to enable google analytics tracking
# TRACKING_ID='UA-999999-99'

SECRET_KEY = ''
from taosecrets import *

