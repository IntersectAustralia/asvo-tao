#!/bin/bash

set -e

TAG=$1

if [ -z "$TAG" ]; then
  echo 'Use version (a tag in remote git repo)'
  exit 1
fi

echo "Deploying to ASV1 version $TAG"
echo 'Assuming you are using ssh properly (https://wiki.intersect.org.au/display/DEV/Use+ssh+Properly)'

DIRS='asvo-tao/web asvo-tao/ui/light-cone asvo-tao/ui/sed asvo-tao/_libs asvo-tao/tao.pip.reqs'
TARGET=/web/vhost/tao.asvo.org.au/taodemo
DEP_DIR=`pwd`

# checks out code into build dir
checkout() {
  cd $DEP_DIR
  test -d build && rm -rf build && echo "Removed existing build dir"
  mkdir build
  cd build
  git clone -b master git@github.com:IntersectAustralia/asvo-tao.git
  cd asvo-tao
  git checkout $TAG
  rm -rf .git
  cd $DEP_DIR
}

environment_setup() {
  echo ">> generating virtual environment."
  cd $DEP_DIR/build
  mkdir TAOENV
  curl -O https://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.9.tar.gz
  tar xvzf virtualenv-1.9.tar.gz
  cd virtualenv-1.9
  found26=`python --version 2>&1 | grep "2.6"`
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

copy_zipstream() {
  # this is for -e package, zipstream, if we have others later, it can be made generic
  zipstream_dir=`pip show zipstream | grep Location`
  zipstream_dir=${zipstream_dir:10}
  mkdir -p $DEP_DIR/build/asvo-tao/_libs
  test -d $DEP_DIR/build/asvo-tao/_libs/zipstream && rm -rf $DEP_DIR/build/asvo-tao/_libs/zipstream
  mkdir $DEP_DIR/build/asvo-tao/_libs/zipstream
  cp -r $zipstream_dir/* $DEP_DIR/build/asvo-tao/_libs/zipstream
  rm -rf $DEP_DIR/build/asvo-tao/_libs/zipstream/.git
}

# usage: transfer <host>
# compresses build/* into asvo.tgz and transfers it to server
# also copies remote.sh and maintenance files
transfer() {
  host=$1
  echo ">> PACKAGING APP FOR $host"
  source $DEP_DIR/build/TAOENV/bin/activate
  cd $DEP_DIR/build
  test -f asvo.tgz && rm -f asvo.tgz && echo "Removed existing .tgz"
  copy_zipstream
  tar -czf asvo.tgz -C $DEP_DIR/build $DIRS
  cd $DEP_DIR
  echo ">> UPLOADING TO $host"
  scp build/asvo.tgz remote.sh $host:~
  HOME_DIR=$(ssh $host 'chmod a+x remote.sh; echo $HOME')
}

# usage: remote_stop <host> <htaccess_flag (optional)>
# copies interim .htaccess file to server and stops django
remote_stop() {
  host=$1
  htaccess_flag=$2
  echo PLEASE PROVIDE taoadmin PASSWORD TO STOP $host
  if [ -n "$htaccess_flag" ]; then
     ssh -t $host 'su taoadmin -c "cp '$HOME_DIR'/maintenance_htaccess '$TARGET'/.htaccess; cp '$HOME_DIR'/maintenance_index.html '$TARGET'/index.html; pkill django; echo Stopped..."'
  else
     ssh -t $host 'su taoadmin -c "pkill django; echo Stopped..."'
  fi
}

# usage: remote_unpack <host>
# executes remote.sh in target server
remote_unpack() {
  host=$1
  echo PLEASE PROVIDE taoadmin PASSWORD TO UNPACK APP IN $host
  ssh -t $host 'su taoadmin -c '\'$HOME_DIR'/remote.sh unpack'\'
}

# usage: remote_install <host>
# executes remote.sh in target server
remote_install() {
  host=$1
  echo PLEASE PROVIDE taoadmin PASSWORD TO RUN INSTALL SCRIPT ON $host
  ssh -t $host 'su taoadmin -c '\'$HOME_DIR'/remote.sh install'\'
}

# usage: remote_restore <host>
remote_restore() {
  host=$1
  echo PLEASE PROVIDE taoadmin PASSWORD TO RESTART $host
  echo ssh -t $host 'su taoadmin -c "cp '$HOME_DIR'/production_htaccess '$TARGET'/.htaccess; rm '$TARGET'/index.html"'
  ssh -t $host 'su taoadmin -c "cp '$HOME_DIR'/production_htaccess '$TARGET'/.htaccess; rm '$TARGET'/index.html"'
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

remote_unpack asv1

# update htaccess in transfer node and stop that one, then stop the other
# remote_stop asv1 htaccess
# remote_stop asv2

# run the install script now, as storage and DB are shared, we need
# to do this in transfer node only
# remote_install asv1

# restores the .htaccess file, again, only transfer node needs to be accessed
# remote_restore asv1

