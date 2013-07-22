#!/usr/bin/env python
"""
Call the workflow command api to demonstrate simulating the backend.

Note that this doesn't demonstrate retrieving data, which can be done with:

    # Get all workflow commands
    curl http://127.0.0.1:8000/api/v1/workflowcommand/
    
    # Get SUBMITTED commands
    curl http://127.0.0.1:8000/api/v1/workflowcommand/?execution_status=submitted
    
    # Get pk=1 command
    curl http://127.0.0.1:8000/api/v1/workflowcommand/1/

(When trying the URLs in the browser, append ?format=json because browser requests application/xml before application/json
 i.e., http://localhost:8000/api/v1/workflowcommand/?format=json )

It also doesn't do any error checking, etc.  The idea is to read the code.
"""

import sys
import requests
import json

base_url = "https://tao.asvo.org.au/taostaging/api/v1/workflowcommand/"

if len(sys.argv) < 5:
    print("usage: {0} wf_id status comment job_id".format(sys.argv[0]))
    exit(0)

wf_id = sys.argv[1]
status = sys.argv[2].upper()
comment = sys.argv[3]
job_id = sys.argv[4]

data = {
        'id': wf_id,
        'execution_status': status,
        'execution_comment': comment,
}

print("Workflow ID: {0}".format(wf_id))
print("Status: {0}".format(status))
print("Comment: {0}".format(comment))
print("Job ID: {0}\n\n".format(job_id))

print("GET URL: {0}".format(base_url))
response = requests.get(base_url)
print("Response: {0}".format(response))
if response.status_code == requests.codes.ok:
    print(json.dumps(json.loads(response.content),
        sort_keys=True, indent=4, separators=(',',':')))

url = base_url + wf_id + '/'
print("PUT URL: {0}".format(url))
response = requests.put(url, data=json.dumps(data), headers={'content-type': "application/json"})
print("Response: {0}".format(response))
print response.headers['content-type']
print response.content
print ">> Note that 204 is the correct response for a successful PUT.\n\n"

print("GET URL: {0}".format(url))
response = requests.get(url)
print("Response: {0}".format(response))
if response.status_code == requests.codes.ok:
    print(json.dumps(json.loads(response.content),
        sort_keys=True, indent=4, separators=(',',':')))

url = base_url + '?job_id=' + job_id # for now just using the same id from args (in reality job_id is different to wf_id)
print("GET URL: {0}".format(url))
response = requests.get(url)
print("Response: {0}".format(response))
if response.status_code == requests.codes.ok:
    print(json.dumps(json.loads(response.content),
        sort_keys=True, indent=4, separators=(',',':')))


url = base_url + '?execution_status=' + status
print("GET URL: {0}".format(url))
response = requests.get(url)
print("Response: {0}".format(response))
if response.status_code == requests.codes.ok:
    print(json.dumps(json.loads(response.content),
        sort_keys=True, indent=4, separators=(',',':')))

