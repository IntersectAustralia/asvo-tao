import os
from tao.models import Job

TAP_IS_AVAILABLE = 'true'
TAP_AVAILABILITY_NOTE = 'TAO TAP Server is available'

execution_duration = 1*24*60*60 # TAP query maximum execution time in seconds

TAP_LANGUAGES = ({'name':'ADQL', 'version':'2.0', 'description':'ADQL 2.0'},
                 {'name':'SQL', 'version':'2008', 'description':'Postgres SQL 9.2'})

TAP_FORMATS   = ({'name':'votable', 'mime':'text/xml', 'description': 'VOTable format'},
                 {'name':'csv', 'mime':'text/xml', 'description': 'CSV'})

TAP_RETENTION_PERIOD = {'default': execution_duration, 'hard': execution_duration}

TAP_EXECUTION_DURATION = {'default': execution_duration, 'hard': execution_duration}

TAP_OUTPUT_LIMIT =  {'default': 1000, 'hard': 100000, 'units': 'rows'}

TAP_CAPABILITIES = ({'id':'tables', 'url':'tables', 'use':'full'},
                    {'id':'capabilities', 'url':'capabilities', 'use':'full'},
                    {'id':'availability', 'url':'availability', 'use':'full'})

TAP_WORKFLOW = 'alpha-light-cone-image'
TAP_OUTPUT_PREFIX = 'tao.output'
TAP_OUTPUT_EXT = 'xml'
TAP_SCHEMA_VERSION = '2.0'

TAP_PASS_THROUGH = True
TAP_ALL_FIELDS = True 
TAP_MODULE_VERSION = 1
TAP_BACKEND_SERVER = 'tao01'

# Map TAO Job statuses to UWS standard
uws_statuses = {
                Job.SUBMITTED:   'QUEUED',
                Job.QUEUED:      'QUEUED',
                Job.IN_PROGRESS: 'EXECUTING',
                Job.COMPLETED:   'COMPLETED',
                Job.ERROR:       'ERROR',
                Job.HELD:        'SUSPENDED'
                }

# Return 'UNKNOWN' status safely if something strange happens 
class JOB_STATUS(dict):
    def __getitem__(self, key):
        if not self.has_key(key):
            return 'UNKNOWN'
        else:
            return dict.__getitem__(self,key)
            
UWS_JOB_STATUS = JOB_STATUS(uws_statuses)


