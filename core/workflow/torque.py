##
## @package torque
## Routines to simplify interaction with the PBS server.
##

import os, shlex, subprocess, logging
import PBSPy.capi as pbs
import dbase

# Get the logger.
logger = logging.getLogger('tao-workflow')

# Configuration.
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
    logger.info('Writing script to "%s".'%script_filename)
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
    logger.info('Submitting job to g2.')
    stdout = subprocess.check_output(shlex.split('ssh g2 \"cd %s; qsub %s\"'%(os.getcwd(), script)))
    pbs_id = stdout[:-1] # remove trailing \n
    logger.info('New job with ID "%s".'%pbs_id)
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
def query(pbs_ids):
    logger.info('Searching for jobs %s.'%str(pbs_ids))
    states = {}
    all_jobs = subprocess.check_output(shlex.split('ssh g2 qstat'))
    lines = all_jobs.splitlines()[2:]
    for line in lines:
        words = line.split()
        if words[0].find('.') == -1:
            continue
        for pbs_id in pbs_ids:
            if words[0][:words[0].find('.')] == pbs_id[:pbs_id.find('.')]:
                states[pbs_id] = words[4]
    if len(states) != len(pbs_ids):
        logger.info('Dropped jobs, flagging as complete.')
        for pbs_id in pbs_ids:
            if pbs_id not in states:
                logger.info('  %s dropped.'%pbs_id)
                states[pbs_id] = 'C'
    logger.info('Found states %s.'%str(states))
    return states

    # server = connect()
    # status = server.statjob(pbs_id)
    # assert len(status) == 1

    # job_state = None
    # for attr in status[0].attribs:
    #     if attr.name == 'job_state':
    #         job_state = attr.value
    #         break
    # assert job_state is not None

    # return job_state
