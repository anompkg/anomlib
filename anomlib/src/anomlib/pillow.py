#!/usr/bin/env python3

"""This library is called Pillow, because it works on things that makes sure that your trust was respected.

It provides hashes for certain things.
It allows you getting some items more safer ways avoiding (i. e. KeyErrors).
Also it lets you avoid way too frequent updates by categorizing things into group and setting a update limits for them.
"""

import hashlib, os, sys

from pathlib import Path

def mkdirs(path):
    if not os.path.exists(path):
        os.makedirs(str(path))

def mkdirs_safely(dir):
    "Make sure that path to directory exists."
    try:
        os.makedirs(str(dir))
    except:
        pass

def getKey(d, key="index"):
    "Get item from dictionary otherwise None"
    with suppress(Exception): d[key]; return _

def hashedString(s, hashTool="sha256"):
    h = hashlib.new(hashTool)
    h.update(s.encode()) # give a encoded string. Makes the String to the Hash 
    return h.hexdigest() # Return the Hash

