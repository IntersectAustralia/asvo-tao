#!/bin/bash

set -e
WORKSPACE="$HOME/.virtualenv"
CUR_DIR=`pwd`

setup_virtualenv() {
test ! -d $WORKSPACE && mkdir -p $WORKSPACE
cd $WORKSPACE/
echo "Setting up virtualenv in $WORKSPACE"
curl -O https://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.9.tar.gz
tar xvzf virtualenv-1.9.tar.gz
cd virtualenv-1.9
found26=`python --version 2>&1 | grep "2.6"`
if [ -n "$found26" ]; then
   python virtualenv.py ../TAO
else
   /usr/bin/env python26 virtualenv.py ../TAO
fi
cd ../TAO/bin
cat activate - > activate-qa <<EOF
export DJANGO_SETTINGS_MODULE=tao.qa
echo "Activated tao.qa"
EOF
chmod a+x activate-qa
}

install_fabric() {
source $WORKSPACE/TAO/bin/activate-qa
pip install fabric
}

deploy() {
source $WORKSPACE/TAO/bin/activate-qa
cd $CUR_DIR
echo fab qa $*
fab qa $*
}

install_libraries() {
source $WORKSPACE/TAO/bin/activate-qa
rm -rf $WORKSPACE/TAO/src/*
cd $CUR_DIR/..
pip install -r tao.pip.reqs
}

web_gendocs() {
source $WORKSPACE/TAO/bin/activate-qa
cd $CUR_DIR/../docs/
./gendoc.sh
cd $CUR_DIR/
./manage.py collectstatic --noinput
}

migrate() {
source $WORKSPACE/TAO/bin/activate-qa
$CUR_DIR/manage.py syncdb --noinput
$CUR_DIR/manage.py migrate --noinput
}

help() {
  echo "Use setup|install|gendocs|migrate on remote"
  echo "Use setup|fabric|deploy <option> on tester machine"
}

if [ -z "$1" ]; then
   help
   exit
fi
command=$1
echo "COMMAND >> $command"
shift
case $command in
  setup)    setup_virtualenv
            ;;
  fabric)  install_fabric
            ;;
  deploy)  deploy $*
            ;;
  install)  install_libraries
            ;;
  gendocs)  web_gendocs
            ;;
  migrate)  migrate
            ;;
  *)        help
            exit 1
            ;;
esac
