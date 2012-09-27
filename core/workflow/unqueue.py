import requests

for ii in range(2):
    requests.put('http://tao.asvo.org.au/taodemo/api/jobs/%d'%(ii + 1), data={'status': 'SUBMITTED'})
