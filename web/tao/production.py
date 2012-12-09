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

SECRET_KEY = ''
from tao.secrets import *

STATIC_URL = '/taodemo/static/'
FILES_BASE = '/mnt/TAOAdmin/'  # please include a trailing slash

EMAIL_HOST = 'gpo.swin.edu.au'
EMAIL_PORT = '25'

EMAIL_FROM_ADDRESS = 'tao.admin@asvo.org.au'

API_ALLOWED_IPS = (
                   '127.0.0.1',
                   '136.186.55.225', # tao01
                   '136.186.55.226', # tao02
                   )
