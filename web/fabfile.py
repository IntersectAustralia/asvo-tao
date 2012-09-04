"""
    Notes:
    * you may want to copy your ssh public keys to the remote hosts (not a task here)
"""
from fabric.api import *
from fabric.context_managers import cd

env.forward_agent = True

# defaults

env.user = 'devel'
env.hosts = ['asvo-qa.intersect.org.au']


# environments

def qa(): # for completeness
    env.user = 'devel'
    env.hosts = ['asvo-qa.intersect.org.au']

def demo():
    env.user = 'devel'
    env.hosts = ['asvo-demo.intersect.org.au']


# tasks

def initial_deploy():
    sudo("yum install git -y")
    run("git clone git@github.com:IntersectAustralia/asvo-tao.git")

def update():
    with cd("asvo-tao/web"):
        run("git pull")
