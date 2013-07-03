"""
==================
tao.development
==================

Settings for development environment
"""

from tao.settings import *

# Configure SMTP Server.
# See https://docs.djangoproject.com/en/dev/topics/email/
EMAIL_HOST = 'localhost'
EMAIL_PORT= '1025'

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
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB'
        }
    }
}
