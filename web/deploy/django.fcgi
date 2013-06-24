#!/bin/bash

# FIXME This is not really a good directory to put eggs...
# export PYTHON_EGG_CACHE=/tmp
export SCRIPT_NAME='/tao/'

# start virtualenv
VPYTHON_DIR=/home/devel/.virtualenv
activate=$VPYTHON_DIR/TAO/bin/activate-qa
source $activate

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
"$DIR/../manage.py" runfcgi !*
