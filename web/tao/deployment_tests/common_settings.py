USERNAME = None
PASSWORD = None
DOWNLOAD_DIR = '/tmp/detest/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s: %(message)s'
        },
    },
    'filters': {
    },
    'handlers': {
        'rotate': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': '/tmp/detest.log',
            'maxBytes': 10000000,
            'backupCount': 5
            },
        'console':{
            'level': 'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
         'detest': {
             'handlers' : ['rotate', 'console'],
             'propagate' : True,
             'level' : 'DEBUG',
         },
    },
#     'root' : {
#         'handlers' : ['rotate', 'console'],
#         'propagate' : True,
#         'level' : 'DEBUG',
#     }
}

