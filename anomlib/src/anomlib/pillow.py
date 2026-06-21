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

def _hash_file(input_file, hashTool="sha256"):
    """Hash file Fearlessly.
    hashTool supports hashlib's hash functions such as md5 or sha512. 
    """
    # input_file = input("Enter the name of the file: ")
    # Note: Open file as 'bytes' not 'str' when 'rb' used.
    # TODO: To encode 'str' into 'bytes' use "text".encode()
    with open(input_file, 'rb') as file:
        text = file.read()
        result = vars(hashlib)[hashTool](text).hexdigest()
    # TODO: It may be "tempting" to return just one hash, but reusing read file object can speed up process.
    # return (md5_hash, sha1_hash, sha256_hash)
    return result

def hash_file(input_file):
    try:
        return _hash_file(input_file)
    except IsADirectoryError:
        return

def hashValue(value, name=None, hashTool="md5"):
    # Hash Value or value
    valueHash = hashedString(value, hashTool)

    # If name is None, False or Empty string: Just return hash
    if not name:
        return valueHash
    
    # Get name from URL if name undefined
    elif name == True:
        # Get Name while expecting that value is either URL or filepath.
        name = value.split("/")[-1]

    return f"{name}@{valueHash}"

