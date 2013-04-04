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
  cp -r $UNPACK_DIR/asvo-tao/* $TARGET/
}

rebuild() {
  echo "Rebuild with buildout..."
  cd $TARGET/web
  python bootstrap.py -v 1.7.0
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
  cd $TARGET/web
  bin/django collectstatic
}

finish() {
  cp $DIR/production_htaccess $TARGET/.htaccess
}

unpack
copy_files
rebuild
db_update
static_update
finish
