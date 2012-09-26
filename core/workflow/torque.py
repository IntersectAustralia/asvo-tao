import os, shlex, subprocess
import PBSPy.capi as pbs
import dbase

server_address = 'pbs.hpc.swin.edu.au'
script_filename = 'pbs_script'
queue = 'gstar'

##
##
##
def connect():
    server = pbs.Server(server_address)
    server.connect()
    return server

##
##
##
def default_params():
    params = {
        'nodes': 1,
        'ppn': 1,
        'wt_hours': 0,
        'wt_minutes': 30,
        'wt_seconds': 0,
    }
    return params

##
##
##
def write_script(params, path='.'):
    filename = os.path.join(path, script_filename)
    with open(filename, 'w') as script:
        script.write('''#!/bin/bash
#PBS -N %(name)s
#PBS -l nodes=%(nodes)d:ppn=%(ppn)d
#PBS -l walltime=%(wt_hours)02d:%(wt_minutes)02d:%(wt_seconds)02d
#PBS -d .
source /usr/local/modules/init/bash
module load openmpi
mpiexec %(pipeline)s params.xml
'''%params)
    return filename

##
##
##
def submit(params, queue=None):
    script = write_script(params)
    stdout = subprocess.check_output(shlex.split('qsub ' + script))
    pbs_id = stdout[:-1] # remove trailing \n
    return pbs_id

##
##
##
def query(pds_id):
    server = connect()
    status = server.statjob(pbs_id)
    assert len(status) == 1

    job_state = None
    for attr in status[0].attribs:
        if attr.name == 'job_state':
            job_state = attr.value
            break
    assert job_state is not None

    return job_state
