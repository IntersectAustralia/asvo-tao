##
## @package torque
## Routines to simplify interaction with the PBS server.
##

import os, shlex, subprocess
import PBSPy.capi as pbs
import dbase

server_address = 'pbs.hpc.swin.edu.au'  # The location of the PBS server.
script_filename = 'pbs_script'          # What to call the generated PBS script.
queue = 'gstar'                         # Which queue to submit to.

##
## Connect to the PBS server.
##
## @returns PBSPy Server class.
##
def connect():
    server = pbs.Server(server_address)
    server.connect()
    return server

##
## Generate a dictionary of default parameters.
##
## @returns Dictionary of default parameters.
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
## Write a PBS script from a parameters dictionary.
##
## @param[IN]  params  Dictionary of parameters.
## @param[IN]  path    Where to write PBS script.
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
module load mpich2 hdf5/x86_76/gnu/1.8.9-mpich2 boost
export PATH=/home/lhodkins/workspace/asvo-tao/science_modules/build-debug/bin:$PATH
export LD_LIBRARY_PATH=/home/lhodkins/workspace/asvo-tao/science_modules/build-debug/lib:$LD_LIBRARY_PATH
mpiexec %(pipeline)s params.xml
'''%params)
    return filename

##
## Submit a PBS job.
##
## @param[IN]  params  Parameter dictionary.
## @returns PBS job identifier.
##
def submit(params):
    script = write_script(params)
    stdout = subprocess.check_output(shlex.split('qsub ' + script))
    pbs_id = stdout[:-1] # remove trailing \n
    return pbs_id

##
## Query a PBS job.
##
## The character returned indicates the job state as follows:
##  Q = queued
##  R = running
##  C = complete
##
## @param[IN]  pbs_id  PBS job identifier.
## @returns A character representing the job state.
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
