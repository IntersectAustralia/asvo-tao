#!/bin/bash

set -e

DIR=`dirname $0`
TARGET=/web/vhost/tao.asvo.org.au/taodemo
UNPACK_DIR=/home/taoadmin/tmpdoc

unpack() {
  echo "Unpacking documentation..."
  test -d $UNPACK_DIR && rm -rf $UNPACK_DIR && echo "Cleaning up $UNPACK_DIR dir"
  mkdir $UNPACK_DIR
  tar -xzf $DIR/asvo-doc.tgz -C $UNPACK_DIR
}

copy_files() {
  echo "Copying files..."
  cp -r $UNPACK_DIR/asvo-tao/* $TARGET/
}

static_update() {
  echo "Updating static resources..."
  cd $TARGET/web
  bin/django collectstatic
}

unpack
copy_files
static_update
