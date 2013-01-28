#! /usr/bin/env python
# -*- coding: utf-8 -*-
from paver.easy import *
import os
import os.path
import subprocess

project_root = os.path.abspath(os.path.dirname(__file__))

@task
def all():
    for f in[clead,build]:
        os.chdir(project_root)
        f()
    print "All task finished!!"
    
@task
def test():
    os.chdir(project_root)
    sh("py.test test")

@task
def test_all():
    os.chdir(project_root)
    sh("tox")

@task
def clean():
    os.chdir(project_root)
    sh("rm -rf pyoauth2.egg-info")
