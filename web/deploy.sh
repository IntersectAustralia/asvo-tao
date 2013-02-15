#!/bin/bash

echo 'Deploying to asv1'
echo 'Assuming you are using ssh properly (https://wiki.intersect.org.au/display/DEV/Use+ssh+Properly)'

DIRS='asvo-tao/web light-cone sed'
TARGET=/web/vhost/tao.asvo.org.au/taodemo
DEP_DIR=`pwd`

# checks out code into build dir
checkout() {
  test -d build && rm -rf build && echo "Removed existing build dir"
  mkdir build
  cd build
  git clone --depth 1 git@github.com:IntersectAustralia/asvo-tao.git
  git clone --depth 1 -b light-cone git@github.com:IntersectAustralia/asvo-tao-ui-modules.git light-cone
  git clone --depth 1 -b sed git@github.com:IntersectAustralia/asvo-tao-ui-modules.git sed
  for d in asvo-tao light-cone sed; do test -d $d/.git && rm -rf $d/.git; done
  cd $DEP_DIR
}

# generate documentation in build directory
generate_documentation() {
  CURRENT=`pwd`
  cd build/asvo-tao/web
  cp -r $DEP_DIR/eggs .
  mkdir src
  cp -r $DEP_DIR/build/light-cone src
  cp -r $DEP_DIR/build/sed src
  cd $DEP_DIR
  cd build/asvo-tao/docs
  ./gendoc.sh
  cd $DEP_DIR
}

# usage: transfer <host>
# compresses build/* into asvo.tgz and transfers it to server
# also copies remote.sh and maintenance files
transfer() {
  host=$1
  test -f asvo.tgz && rm -f asvo.tgz && echo "Removed existing .tgz"
  tar -czf asvo.tgz -C build $DIRS
  scp asvo.tgz remote.sh deploy/maintenance_htaccess deploy/maintenance_index.html deploy/production_htaccess $host:~
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

# usage: remote_install <host>
# executes remote.sh in target server
remote_install() {
  host=$1
  echo PLEASE PROVIDE taoadmin PASSWORD TO RUN INSTALL SCRIPT ON $host
  ssh -t $host 'su taoadmin -c '\'$HOME_DIR'/remote.sh'\'
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

generate_documentation

# underlying storage is shared, so we only need to access one node
# this is the transfer node mentioned below
transfer asv1

# update htaccess in transfer node and stop that one, then stop the other
remote_stop asv1 htaccess
remote_stop asv2

# run the install script now, as storage and DB are shared, we need
# to do this in transfer node only
remote_install asv1

# restores the .htaccess file, again, only transfer node needs to be accessed
remote_restore asv1

