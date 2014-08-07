#!/bin/bash

set -e

ENVIRONMENT=$1
TAG=$2
GIT_BRANCH=master
GIT_URL=git@github.com:IntersectAustralia/asvo-tao.git

check_params() {
if [ -z "$TAG" -o -z "$ENVIRONMENT" ]; then
  echo 'Usage: deploy2.sh <environment> <tag>'
  echo '<environment> = production|stagin'
  echo '<tag> = tag from git'
  exit 1
fi

if [ ! "$ENVIRONMENT" = "production" -a ! "$ENVIRONMENT" = "staging" ]; then
  echo 'Error: use production or staging for environment'
  exit 1
fi

case $ENVIRONMENT in
  production)
    TARGET=/web/vhost/tao.asvo.org.au/tao
    BACKUP_DIR=/home/taoadmin/sites/production
    ;;
  staging)
    TARGET=/web/vhost/tao.asvo.org.au/taostaging
    BACKUP_DIR=/home/taoadmin/sites/staging
    ;;
  *)
    exit 1
esac

case `which python` in
  *$ENVIRONMENT*)
    ;;
  *)
    echo "You need to activate the right virtual environment!"
    exit 1
esac

echo "Deploying to $ENVIRONMENT version $TAG to $TARGET"
}

# backup master db
backup_db() {
  echo "Backup up master db..."
  cd $TARGET/asvo-tao/web
  ./manage.py dumpscript > $BACKUP_DIR/masterdb.py
}

migrate_db() {
  echo "Migrate DB >>> "
  cd $TARGET/asvo-tao/web
  ./manage.py syncdb
  ./manage.py sync_rules
  ./manage.py migrate 
}
# checks out code into TARGET
checkout() {
  cd $TARGET
  if [ ! -d asvo-tao ]; then
    git clone -b $GIT_BRANCH $GIT_URL asvo-tao
  fi
  cd asvo-tao
  git fetch
  git checkout $TAG
}

environment_setup() {
  echo ">> installing packages into $ENVIRONMENT"
  cd $TARGET/asvo-tao
  pip install -r tao.pip.reqs
  if [ -z "`pip show taosecrets`" ]; then
    echo 'Please install taosecrets for this environment'
    exit 1
  fi
}

generate_documentation() {
  cd $TARGET/asvo-tao/docs
  ./gendoc.sh
  cd $TARGET/asvo-tao/web
  ./manage.py collectstatic
}

# usage: remote_stop <host> <htaccess_flag (optional)>
# copies interim .htaccess file to server and stops django
server_restart() {
  host=$1
  htaccess_flag=$2
  echo PLEASE PROVIDE taoadmin PASSWORD TO STOP $host
  if [ -n "$htaccess_flag" ]; then
     ssh -t $host 'su taoadmin -c "cp '$HOME_DIR'/maintenance_htaccess '$TARGET'/.htaccess; cp '$HOME_DIR'/maintenance_index.html '$TARGET'/index.html; pkill django; echo Stopped..."'
  else
     ssh -t $host 'su taoadmin -c "pkill django; echo Stopped..."'
  fi
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

check_params

backup_db

checkout

migrate_db

environment_setup

generate_documentation

echo "Killing service in this host, it restarts automatically"
killall /home/taoadmin/sites/$ENVIRONMENT/TAO/bin/python
cd $TARGET/asvo-tao/web
find . -name "*.pyc" -exec rm -f {} \;

# update htaccess in transfer node and stop that one, then stop the other
# remote_stop asv1 htaccess
# remote_stop asv2

# run the install script now, as storage and DB are shared, we need
# to do this in transfer node only
# remote_install asv1

# restores the .htaccess file, again, only transfer node needs to be accessed
# remote_restore asv1

