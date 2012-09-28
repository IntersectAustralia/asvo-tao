#!/usr/bin/env python

import os, shlex, subprocess, time, logging
import requests
from torque import *
import dbase

# Configuration.
work_dir = '/lustre/projects/p014_swin/FTP'
log_path = '/lustre/projects/p014_swin/logs/workflow.log'
sleep_time = 180

# Setup the logger.
def setup_logging():
    logger = logging.getLogger('tao-workflow')
    file_handler = logging.FileHandler(log_path)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    # console_handler = logging.StreamHandler()
    # console_handler.setFormatter(formatter)
    # logger.addHandler(console_handler)
    logger.setLevel(logging.DEBUG)
    return logger
logger = setup_logging()

# Define the request API.
url_base = 'http://tao.asvo.org.au/taodemo/api/'
api = {
    'get': url_base + 'jobs/status/submitted',
    'update': url_base + 'jobs/%d',
}
auth = ('user', 'pass')


##
##
##
def json_handler(resp):
    for json in resp.json:
        path = os.path.join('jobs', json['user']['username'], str(json['id']))
        os.makedirs(path)
        old_dir = os.getcwd()
        os.chdir(path)

        with open('params.xml', 'w') as file:
            file.write(json['parameters'])

        params = default_params()
        params['name'] = json.get('name', 'tao_' + json['user']['username'] + '_' + str(json['id']))
        params['pipeline'] = 'skymaker' #json['pipeline']
        if 'nodes' in json:
            params['nodes'] = json['nodes']
        if 'ppn' in json:
            params['ppn'] = json['ppn']
        pbs_id = submit(params)

        os.chdir(old_dir)
        dbase.add_job(path, pbs_id, json['id'])

        # Mark job as queued.
        requests.put(api['update']%json['id'], data={'status': 'QUEUED'})

    return len(resp.json)

##
##
##
def xml_handler(resp):
    xml = resp.xml
    assert 0

# Define content handler mapping.
content_handlers = {
    'application/json': json_handler,
    'application/xml': xml_handler,
}

# Entry point for the main workflow system.
if __name__ == '__main__':

    # Change location to the working directory.
    os.chdir(work_dir)

    # Load any existing database information.
    dbase.load_jobs()

    # Repeat forever.
    logger.info('Entering main loop.')
    while 1:

        # Check for any newly submitted jobs.
        logger.info('Checking for new jobs.')
        new_jobs = 0
        resp = requests.get(api['get'])
        content_type = resp.headers['content-type']
        for k, v in content_handlers.iteritems():
            if content_type[:len(k)] == k:
                new_jobs = v(resp)
        logger.info('Found %d new jobs.'%new_jobs)

        # Check for changes in status of running jobs.
        logger.info('Checking existing jobs.')
        ids = dbase.get_job_ids()
        rids = dict([(v, k) for k, v in ids.iteritems()])
        states = query(ids.values())
        for pbs_id, state in states.iteritems():
            tao_id = rids[pbs_id]
            info = dbase.get_job(tao_id)
            if state != info[2]:
                logger.info('Job %d\'s state changed to %s.'%(tao_id, state))
                info[2] = state
                dbase.save_jobs()
                data = {}
                if state == 'R':
                    state = 'IN_PROGRESS'
                else:
                    logger.info('Job complete, deleting from dbase.')
                    state = 'COMPLETED'
                    data['output_path'] = info[1]
                    dbase.delete_job(tao_id)
                data['status'] =  state
                logger.info('Updating server.')
                requests.put(api['update']%tao_id, data=data)

        # Sleep for a period.
        logger.info('Going to sleep for %d seconds.'%sleep_time)
        time.sleep(sleep_time)
