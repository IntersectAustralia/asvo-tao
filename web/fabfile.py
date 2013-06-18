"""
    Notes:
    * you may want to copy your ssh public keys to the remote hosts (not a task here)
    * you may need to disable selinux
    * assumes deploying to the user's home directory
    * probably want to setup a root password on your mysql server
"""
from fabric.api import *
from fabric.context_managers import cd
from fabric.contrib.files import exists

env.forward_agent = True

# environments

def qa():
    env.user = 'devel'
    env.hosts = ['asvo-qa.intersect.org.au']
    env.target_env = 'qa'


def demo():
    env.user = 'devel'
    env.hosts = ['asvo-demo.intersect.org.au']
    env.target_env = 'demo'


# defaults to QA settings
qa()


# tasks

def _create_mysql_user_and_database():
    # TODO don't hard-code username/password/database name
    run("""echo "create user 'tao'@'localhost' identified by 'tao'; grant all privileges on tao.* to 'tao'@'localhost'; flush privileges;" | mysql -uroot """)
    run("""echo "create database tao;" | mysql -utao --password=tao""")

def install_software():
    sudo("yum install -y git mod_fcgid mysql-server mysql-devel gcc python-devel postfix doxygen")
    sudo("chkconfig mysqld on")
    sudo("chkconfig httpd on")
    sudo("chkconfig postfix on")
    sudo("service mysqld start")
    sudo("service postfix start")

def create_database():
    _create_mysql_user_and_database()

def run_git(git_command):
    run("eval `ssh-agent`; ssh-add /home/devel/.ssh/id_rsa; " + git_command)

def initial_setup():
    if exists("asvo-tao"):
        run("rm -rf asvo-tao")
    run_git("git clone git@github.com:IntersectAustralia/asvo-tao.git")
    run("chmod o+rx /home/{user}/asvo-tao".format(user=env.user))
    with cd("asvo-tao/web"):
        run_git("git checkout work")
        run_git("git pull origin work")
        run("./qa.sh setup")

def update():
    with cd("asvo-tao"):
        run_git("git checkout work")
        run_git("git pull origin work")
    with cd("asvo-tao/web"):
        run("./qa.sh install")
        run("./qa.sh gendocs")
        run("./qa.sh migrate")
    with cd("asvo-tao/web"):
        sudo("cp deploy/httpd/tao_{target_env}_httpd.conf /etc/httpd/conf.d/tao_httpd.conf".format(target_env=env.target_env))
    sudo("service httpd graceful")

def create_test_admin_users():
    with cd("asvo-tao/web"):
        run("bin/django loaddata test_data/test_users.json")
