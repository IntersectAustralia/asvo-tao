#!/usr/bin/env python

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

##
##
##
def xml_handler(resp):
    xml = resp.xml

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
