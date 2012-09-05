#!/bin/bash

# script to be used by mod_fcgid
# run after buildout has installed the "django" part

# FIXME This is not really a good directory to put eggs...
export PYTHON_EGG_CACHE=/tmp
export SCRIPT_NAME='/tao/'

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
"$DIR/../bin/django" runfcgi !*
