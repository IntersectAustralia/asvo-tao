#!/usr/bin/env python

import shlex, subprocess, time
import requests
import torque

# Define the request API.
url_base = 'https://tao.swin.edu.au/taodemo/api/'
api = {
    'get': url_base + 'jobs/status/submitted',
    'update': url_base + 'jobs/update',
}
auth = ('user', 'pass')

# How long to sleep inbetween checks? (in seconds)
sleep_time = 10

##
##
##
def json_handler(resp):
    json = resp.json

    path = os.path.join('jobs', json['user']['username'], json['id'])
    os.makedirs(path)
    old_dir = os.getcwd()
    os.chdir(path)

    with open('params.xml', 'w') as file:
        file.write(json['parameters'])

    params = default_params()
    params['name'] = json['name']
    params['pipeline'] = 'skymaker' #json['pipeline']
    if 'nodes' in json:
        params['nodes'] = json['nodes']
    if 'ppn' in json:
        params['ppn'] = json['ppn']
    pbs_id = submit(params)

    os.chdir(old_dir)
    dbase.add_job(path, pbs_id, json['id'])

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
    import pdb
    pdb.set_trace()

    # Repeat forever.
    while 1:

        # Check for any newly submitted jobs.
        resp = requests.get(api['get'])
        content_type = resp.headers['content-type']
        for k,v in content_handlers:
            if content_type[:len(k)] == k:
                v(resp)

        # Check for changes in status of running jobs.
        for tao_id, pbs_id in dbase.iter_active():
            pass

        # Sleep for a period.
        time.sleep(sleep_time)
