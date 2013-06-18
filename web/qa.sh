#!/bin/bash

set -e
WORKSPACE="~/.virtualenv"
CUR_DIR=`pwd`

setup_virtualenv() {
cd $WORKSPACE/
echo "Setting up virtualenv in $WORKSPACE"
curl -O https://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.9.tar.gz
tar xvzf virtualenv-1.9.tar.gz
cd virtualenv-1.9
/usr/bin/env python26 virtualenv.py ../TAO
cd ../TAO/bin
cat activate - > activate-qa <<EOF
export DJANGO_SETTINGS_MODULE=tao.qa
echo "Activated tao.qa"
EOF
chmod a+x activate-qa
}

install_libraries() {
source $WORKSPACE/TAO/bin/activate-qa
rm -rf $WORKSPACE/TAO/src/*
pip install -r tao.pip.reqs
}

web_gendoc() {
source $WORKSPACE/TAO/bin/activate-qa
. $CUR_DIR/../docs/gendoc.sh
$CUR_DIR/manage.py collectstatic --noinput
}

migrate() {
source $WORKSPACE/TAO/bin/activate-qa
$CUR_DIR/manage.py syncdb --noinput
$CUR_DIR/manage.py migrate --noinput
}

command=$1
echo "COMMAND >> $command"
shift
case $command in
  setup)    setup_virtualenv
            ;;
  install)  install_libraries
            ;;
  gendocs)  web_gendocs
            ;;
  migrate)  migrate
            ;;
  *)        echo "setup|install|gendocs|migrate valid options"
            exit 1
            ;;
esac
