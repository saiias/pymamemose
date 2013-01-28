#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from setuptools import setup, Command

def read_file(name):
    path = os.path.join(os.path.dirname(__file__),name)
    f = open(os.path.abspath(path),'r')
    data = f.read()
    f.close()
    return data

short_description ="Simple memo tool for RestructuredText"

try:
    long_description = read_file("README.rst")
except IOError:
    long_description = ""
    
version = "0.0.1"

classifiers=[
    'Development Status :: 2 - Pre-Alpha',
    'Environment :: Console',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Topic :: Software Development :: Documentation',
    'Topic :: Utilities',
    ]

install_requires = [
    'distribute'
    ]
    

if sys.version_info[0:2] == (2, 6):
    install_requires.append('argparse')



setup(
    name = "pymamemose",
    version =version,
    url ="https://github.com/saiias/pymamemose",
    license = "New BSD",
    author ="Yuki Saitoh",
    author_email = "saiass0708 at gmail.com",
    description = short_description,
    long_description = long_description,
    install_requires = install_requires,
    packages=['pymamemose'],
    package_data={},
    entry_points = {
        'console_scripts':["pymamemose = pymamemose:command"]
        },
    extras_require =dict(
        test=['pytest>=2.3'
              ]
        ),
    test_suite = "test.suite",
    tests_require=["pytest"]    
    )
