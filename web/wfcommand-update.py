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

base_url = "http://127.0.0.1:8000/api/v1/workflowcommand/"

if len(sys.argv) < 4:
    print("usage: {0} job_id status comment".format(sys.argv[0]))
    exit(0)

job_id = sys.argv[1]
status = sys.argv[2]
comment = sys.argv[3]

data = {
        'id': job_id,
        'execution_status': status,
        'execution_comment': comment,
}
print("Job ID: {0}".format(job_id))
print("Status: {0}".format(status))
print("Comment: {0}".format(comment))

print("URL: {0}".format(base_url))
response = requests.get(base_url)
print("Response: {0}".format(response))

url = base_url + job_id
print("URL: {0}".format(url))
response = requests.put(url, data)
print("Response: {0}".format(response))

url = base_url + '?execution_status=' + status
print("URL: {0}".format(url))
response = requests.get(url)
print("Response: {0}".format(response))