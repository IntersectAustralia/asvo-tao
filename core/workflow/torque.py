import PBSPy.capi as pbs

server_address = 'pbs.hpc.swin.edu.au'
script_filename = 'pbs_script'

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
def setup_params():
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
        script.write('''#!/bin/tcsh
#PBS -N %(name)s
#PBS -l nodes=%(nodes)d:ppn=%(ppn)d
#PBS -l walltime=%(wt_hours)02d:%(wt_minutes)02d:%(wt_seconds)02d
#PBS -d .
module load openmpi
mpiexec %(pipeline)s
'''%params)
    return filename

##
##
##
def submit(params, user, queue=None):
    os.chdir(os.path.join('jobs', user))
    script = write_script(params)
    server = connect()
    # server.submit(script=script, queue=queue)
    server.disconnect()
