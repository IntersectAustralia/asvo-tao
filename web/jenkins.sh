#!/bin/bash

set -e

if [ -z "$WORKSPACE" ]; then
        echo "Guessing WORKSPACE is .."
        WORKSPACE='..'
fi

cd $WORKSPACE/web/
/usr/bin/env python bootstrap.py
bin/buildout
bin/django test tao --settings=tao.test
