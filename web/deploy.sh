#!/bin/bash

echo 'Deploying to asv1'
echo 'Assuming you are using ssh propery (https://wiki.intersect.org.au/display/DEV/Use+ssh+Properly)'

DIRS='asvo-tao/web light-cone sed'

checkout() {
  test -d build && rm -rf build && echo "Removed existing build dir"
  mkdir build
  cd build
  git clone --depth 1 git@github.com:IntersectAustralia/asvo-tao.git
  git clone --depth 1 -b light-cone git@github.com:IntersectAustralia/asvo-tao-ui-modules.git light-cone
  git clone --depth 1 -b sed git@github.com:IntersectAustralia/asvo-tao-ui-modules.git sed
  for d in asvo-tao light-cone sed; do test -d $d/.git && rm -rf $d/.git; done
  cd ..
}

transfer() {
  test -f asvo.tgz && rm -f asvo.tgz && echo "Removed existing .tgz"
  tar -czf asvo.tgz -C build $DIRS
  scp asvo.tgz remote.sh $1:~
  ssh $1 'chmod a+x remote.sh'
  HOME_DIR=$(ssh $1 'echo $HOME')
}

remote_install() {
  echo PLEASE PROVIDE taoadmin PASSWORD TO CONTINUE
  ssh -t $1 'su taoadmin -c '\'$HOME_DIR'/remote.sh'\'
}

remote_reset() {
  echo PLEASE PROVIDE taoadmin PASSWORD TO RESTART $1
  ssh -t $1 'su taoadmin -c "pkill django"'
}

checkout
# underlying storage is shared, so we only need to access one node
transfer asv1
remote_install asv1
# still we need to reset both nodes
remote_reset asv1
remote_reset asv2
