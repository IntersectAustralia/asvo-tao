#!/usr/bin/env python

import os, shlex, subprocess, time
import requests
from torque import *
import dbase

# Define the request API.
url_base = 'http://tao.asvo.org.au/taodemo/api/'
api = {
    'get': url_base + 'jobs/status/submitted',
    'update': url_base + 'jobs/%d',
}
auth = ('user', 'pass')

# How long to sleep inbetween checks? (in seconds)
sleep_time = 10

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
        # pbs_id = submit(params)

        os.chdir(old_dir)
        # dbase.add_job(path, pbs_id, json['id'])

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

    # Load any existing database information.
    dbase.load_jobs()

    # Repeat forever.
    while 1:

        # Check for any newly submitted jobs.
        print 'Checking for new jobs.'
        new_jobs = 0
        resp = requests.get(api['get'])
        content_type = resp.headers['content-type']
        for k, v in content_handlers.iteritems():
            if content_type[:len(k)] == k:
                new_jobs = v(resp)
        if new_jobs:
            print '  ' + str(new_jobs) + ' new jobs.'

        # Check for changes in status of running jobs.
        print 'Checking existing jobs.'
        for tao_id, info in dbase.iter_active():
            state = query(info[0])
            if state != info[2]:
                info[2] = state
                dbase.save()
                if state == 'R':
                    state = 'IN_PROGRESS'
                else:
                    state = 'COMPLETED'
                    dbase.delete_job(tao_id)
                requests.put(api['update']%tao_id, data={'status': state})

        # Sleep for a period.
        print 'Sleeping.'
        time.sleep(sleep_time)
