#!/bin/bash

DIR=`dirname $0`
TARGET=/web/vhost/tao.asvo.org.au/taodemo
TARGET_BACKUP=/web/vhost/tao.asvo.org.au/taodemo-backup

unpack() {
  echo "Unpacking..."
  cd ~
  test -d tmp && rm -rf tmp && echo "Cleaning up tmp dir"
  mkdir tmp
  tar -xzf $DIR/asvo.tgz -C tmp
}

copy_files() {
  cd ~
  test -d $TARGET_BACKUP && rm -rf $TARGET_BACKUP
  mv $TARGET $TARGET_BACKUP
  mkdir -p $TARGET
  cp -r tmp/asvo-tao/web $TARGET/
  mkdir -p $TARGET/web/src
  cp -r tmp/light-cone $TARGET/web/src/
  cp -r tmp/sed $TARGET/web/src/
  cp tmp/asvo-tao/web/deploy/production_htaccess $TARGET/.htaccess
}

rebuild() {
  echo "Rebuild w/ buildout..."
  cd $TARGET/web
  python bootstrap.py
  bin/buildout -c buildout_production.cfg
}

dbupdate() {
  echo "Updating DB..."
  bin/django syncdb
  bin/django migrate
  bin/django sync_rules
  bin/django collectstatic
}

restart() {
  echo "Force restart w/ SIGTERM..."
  pkill django
}

unpack
copy_files
rebuild
dbupdate
restart