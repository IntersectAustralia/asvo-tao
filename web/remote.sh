#!/bin/bash

DIR=`dirname $0`
TARGET=/web/vhost/tao.asvo.org.au/taodemo
TARGET_BACKUP=/web/vhost/tao.asvo.org.au/taodemo-backup
UNPACK_DIR=/home/taoadmin/tmp

unpack() {
  echo "Unpacking..."
  test -d $UNPACK_DIR && rm -rf $UNPACK_DIR && echo "Cleaning up $UNPACK_DIR dir"
  mkdir $UNPACK_DIR
  tar -xzf $DIR/asvo.tgz -C $UNPACK_DIR
}

copy_files() {
  echo "Copying files..."
  test -d $TARGET_BACKUP && rm -rf $TARGET_BACKUP
  mv $TARGET $TARGET_BACKUP
  mkdir -p $TARGET
  cp -r $UNPACK_DIR/asvo-tao/web $TARGET/
  mkdir -p $TARGET/web/src
  cp -r $UNPACK_DIR/light-cone $TARGET/web/src/
  cp -r $UNPACK_DIR/sed $TARGET/web/src/
}

rebuild() {
  echo "Rebuild w/ buildout..."
  cd $TARGET/web
  python bootstrap.py
  bin/buildout -c buildout_production.cfg
}

db_update() {
  echo "Updating DB..."
  bin/django syncdb
  bin/django migrate
  bin/django sync_rules
}

static_update() {
  echo "Updating static resources..."
  bin/django collectstatic
}

unpack
copy_files
rebuild
db_update
static_update