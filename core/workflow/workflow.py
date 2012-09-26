#!/usr/bin/env python

import shlex, subprocess
import requests
import torque

# Define the request API.
url_base = 'https://tao.swin.edu.au/api/'
api = {
    'get': url_base + 'jobs/get',
    'update': url_base + 'jobs/update',
}
auth = ('user', 'pass')

##
##
##
def json_handler(resp):
    json = resp.json

    path = os.path.join('jobs', json['user'], json['id'])
    os.makedirs(path)
    old_dir = os.getcwd()
    os.chdir(path)

    with open('params.xml', 'w') as file:
        file.write(json['xml'])

    params = default_params()
    params['name'] = json['name']
    params['pipeline'] = json['pipeline']
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

##
##
##
if __name__ == '__main__':
    resp = requests.get('http://www.google.com')
    content_type = resp.headers['content-type']
    for k,v in content_handlers:
        if content_type[:len(k)] == k:
            v(resp)
