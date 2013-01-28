#! /usr/bin/env python
# -*- coding: utf-8 -*-

from pymamemose import *
import re

"""
大域関数
"""
def test_isRest():
    pat = re.compile(".(rst|rest|txt)$")
    assert isMatchedFile(pat,"test.rst") ==True
    
def test_isNotRest():
    pat = re.compile(".(rst|rest|txt)$")
    assert isMatchedFile(pat,"test.tex") ==False

def test_isIgnore():
    pat = re.compile("TAGS")
    assert isMatchedFile(pat,"TAGS") ==True

def test_isNotIgnore():
    pat = re.compile("TAGS")
    assert isMatchedFile(pat,"test.rst") ==False

