#!/bin/bash

set -e

DIR=`dirname $0`
TARGET=/web/vhost/tao.asvo.org.au/taodemo
UNPACK_DIR=~/tmpdoc
VPYTHON_DIR=~/.virtualenv

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

environment_setup() {
  cd $TARGET/
  activate=$VPYTHON_DIR/TAOENV/bin/activate
  source $activate
  echo ">> virtual environment $active active"
}

static_update() {
  echo "Updating static resources..."
  cd $TARGET/web
  ./manage.py collectstatic
}

unpack

copy_files

environment_setup

static_update
