#!/bin/bash

# FIXME This is not really a good directory to put eggs...
# export PYTHON_EGG_CACHE=/tmp
export SCRIPT_NAME='/taodemo/'

# start virtualenv
VPYTHON_DIR=/home/taoadmin/.virtualenv
activate=$VPYTHON_DIR/TAOENV/bin/activate
source $activate

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
"$DIR/../manage.py" runfcgi !*
