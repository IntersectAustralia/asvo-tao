#!/bin/bash

set -e

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
  echo "Backing up database in $TARGET_BACKUP/dump.py. Use to restore if something goes wrong"
  bin/django dumpscript > $TARGET/dump.py
  test -d $TARGET_BACKUP && rm -rf $TARGET_BACKUP
  mv $TARGET $TARGET_BACKUP
  mkdir -p $TARGET
  echo "Copying files..."
  cp -r $UNPACK_DIR/asvo-tao/* $TARGET/
}

rebuild() {
  echo "Rebuild with buildout..."
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
