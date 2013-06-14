#!/bin/bash

set -e

if [ -z "$WORKSPACE" ]; then
        echo "Guessing WORKSPACE is .."
        WORKSPACE='..'
fi

cd $WORKSPACE/
echo "Setting up virtualenv in $WORKSPACE"
curl -O https://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.9.tar.gz
tar xvzf virtualenv-1.9.tar.gz
cd virtualenv-1.9
/usr/bin/env python26 virtualenv.py ../TAO
cd ../TAO/bin
cat activate - > activate-qa <<EOF
export DJANGO_SETTINGS_MODULE=tao.test
EOF
chmod a+x activate-qa
source activate-qa
cd $WORKSPACE/
rm -rf $WORKSPACE/TAO/src/*
pip install -r tao.pip.reqs
cd $WORKSPACE/web
./manage.py test tao -v2
