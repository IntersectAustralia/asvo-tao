from tao.settings import *
DEBUG=True
TEMPLATE_DEBUG=DEBUG

SOUTH_TESTS_MIGRATE = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': ':memory:',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

FILES_BASE = '/tmp/'  # please include a trailing slash

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'


INSTALLED_APPS += (
    'django_nose',
)

NOSE_ARGS = ['--with-xunit']
