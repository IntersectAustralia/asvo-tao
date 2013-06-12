#!/bin/bash

set -e
set -v

TAG=$1

if [ -z "$TAG" ]; then
  echo 'Use version (a tag in remote git repo)'
  exit 1
fi

echo "This script only deploys documentation to ASV1 version $TAG"
echo 'Assuming you are using ssh properly (https://wiki.intersect.org.au/display/DEV/Use+ssh+Properly)'

DIRS='static/docs'
TARGET=/web/vhost/tao.asvo.org.au/taodemo
DEP_DIR=`pwd`

# checks out code into build dir
checkout() {
  cd $DEP_DIR
  test -d build && rm -rf build && echo "Removed existing build dir"
  mkdir build
  cd build
  git clone -b master https://github.com/IntersectAustralia/asvo-tao.git
  cd asvo-tao
  git checkout $TAG
  rm -rf .git
  cd $DEP_DIR
}

environment_setup() {
  echo ">> generating virtual environment."
  cd $DEP_DIR/build
  mkdir TAOENV
  curl -O https://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.9.1.tar.gz
  tar xvzf virtualenv-1.9.1.tar.gz
  cd virtualenv-1.9.1
  found26=`python --version 2>&1 | grep "2.[67]"`
  if [ -n "$found26" ]; then
      python virtualenv.py ../TAOENV
  else
      /usr/bin/env python26 virtualenv.py ../TAOENV
  fi
  cd $DEP_DIR/build
  source TAOENV/bin/activate
  echo ">> virtual environment active."
  echo ">> installing packages now."
  cd $DEP_DIR/build/asvo-tao
  pip install -r tao.pip.reqs
}

generate_documentation() {
  cd $DEP_DIR/build/asvo-tao/docs
  ./gendoc.sh
}

# usage: transfer <host>
# compresses build/* into asvo.tgz and transfers it to server
# also copies remote.sh and maintenance files
transfer() {
  host=$1
  echo ">> PACKAGING docs FOR $host"
  source $DEP_DIR/build/TAOENV/bin/activate
  cd $DEP_DIR/build
  test -f asvo-doc.tgz && rm -f asvo-doc.tgz && echo "Removed existing asvo-doc.tgz"
  tar -czf asvo-doc.tgz -C $DEP_DIR/build asvo-tao/web/tao/static/docs
  cd $DEP_DIR
  echo ">> UPLOADING TO $host"
  scp build/asvo-doc.tgz remotedoc.sh $host:~
  HOME_DIR=$(ssh $host 'chmod a+x remotedoc.sh; echo $HOME')
}

# usage: remote_install <host>
# executes remote.sh in target server
remote_install() {
  host=$1
  echo PLEASE PROVIDE taoadmin PASSWORD TO RUN INSTALL DOCUMENTATION SCRIPT ON $host
  ssh -t $host 'su taoadmin -c '\'$HOME_DIR'/remotedoc.sh'\'
}

#
# -- main --
#

checkout

environment_setup

generate_documentation

# underlying storage is shared, so we only need to access one node
# this is the transfer node mentioned below
transfer asv1

# run the install script now, as storage and DB are shared, we need
# to do this in transfer node only
#remote_install asv1


