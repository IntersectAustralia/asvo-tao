#!/bin/bash

set -e

DIR=`dirname $0`
TARGET=/web/vhost/tao.asvo.org.au/taodemo
BACKUPS=~/backups
UNPACK_DIR=~/tmp
VPYTHON_DIR=~/.virtualenv

unpack() {
  echo "Unpacking..."
  test -d $UNPACK_DIR && rm -rf $UNPACK_DIR && echo "Cleaning up $UNPACK_DIR dir"
  mkdir $UNPACK_DIR
  tar -xzf $DIR/asvo.tgz -C $UNPACK_DIR
}

backup_current() {
  # copy current code base
  TEMPDIR=`date +%y.%m.%d_%H.%M.%S`
  TEMPDIR=$BACKUPS/$TEMPDIR
  mkdir -p $TEMPDIR
  cp -r $TARGET $TEMPDIR
  # copy current environment
  cp -r $VPYTHON_DIR/TAOENV $TEMPDIR
  # backup db using current environment
  source $TEMPDIR/TAOENV/bin/activate
  cd $TEMPDIR/web/
  ./manage.py dumpscript > $TEMPDIR/dump.py
}

copy_files() {
  test -d $TARGET && rm -rf $TARGET/*
  echo "Copying files..."
  cp -r $UNPACK_DIR/asvo-tao/* $TARGET/
}

customize() {
  # custom env for production
  # 2. pip reqs
  cat $TARGET/tao.pip.reqs | egrep -v '^\-e' > $TARGET/tao-prod.pip.reqs
  cat >> $TARGET/tao-prod.pip.reqs <<EOF
   -e $TARGET/_libs/zipstream
EOF
}

environment_setup() {
  cd $TARGET/
  test ! -d $VPYTHON_DIR && mkdir $VPYTHON_DIR
  activate=$VPYTHON_DIR/TAOENV/bin/activate
  if [ ! -d "$VPYTHON_DIR/virtualenv-1.9" ]; then
    echo ">> downloading virtualenv"
    found26=`python --version 2>&1 | grep "2.6"`
    cd $VPYTHON_DIR
    curl -O https://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.9.tar.gz
    tar xvzf virtualenv-1.9.tar.gz
    cd virtualenv-1.9
    if [ -n "$found26" ]; then
        python virtualenv.py ../TAOENV
    else
        /usr/bin/env python26 virtualenv.py ../TAOENV
    fi
    cat >> $activate <<EOF2
        export DJANGO_SETTINGS_MODULE=tao.production
EOF2
  fi
  source $activate
  customize
  echo ">> virtual environment $active active"
  echo ">> installing packages now."
  cd $TARGET/
  pip install -r tao-prod.pip.reqs
  # install secrets
  cd ~/etc-tao
  pip install -e .
}

db_update() {
  echo "Updating DB..."
  cd $TARGET/web/
  ./manage.py syncdb
  ./manage.py migrate
  ./manage.py sync_rules
}

static_update() {
  echo "Updating static resources..."
  cd $TARGET/web
  ./manage.py collectstatic
}

finish() {
  cp $DIR/production_htaccess $TARGET/.htaccess
}

if [ "$1" = "unpack" ]; then
  unpack
  exit
fi

if [ "$1" = "install" ]; then
  backup_current
  copy_files
  environment_setup
  db_update
  static_update
  finish
  exit
fi

if [ "$1" = "recover" ]; then
  copy_backup
  activate_virtualenv
  db_restore
fi

echo "ERROR >> use remote.sh unpack|install"
exit 1