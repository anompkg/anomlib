#!/usr/bin/env python3
# This file is part of 4g, the forge client.  (coding: utf-8)
# License: GNU Lesser GPL version 3, see the file "AUTHORS" for details.

# =====================
# This file originally got inspiration from ranger's main python script.
# ranger.py can be executed as python but also sourced in bash which is majestic.

# =====================
# This embedded bash script can be executed by sourcing this file.
# It will cd to ranger's last location after you exit it.
# The first argument specifies the command to run ranger, the
# default is simply "ranger". (Not this file itself!)
# The other arguments are passed to ranger.
"""":
anomtool="${1:-./4g}"
if [ -n "$1" ]; then
    shift
fi
"$anomtool" "${@:-$PWD}"
return "$?"
"""

# import optparse
# import subprocess
# import textwrap
# import argparse
# import getopt
# import logging

import os
import sys

import anomlib.builtin.do
import anomlib.builtin.picload
import anomlib.pillow
import anomlib.prmparser
from anomlib.prmparser import ParamParser


CONF = "params/anomtool.toml"
# CONF = os.path.abspath(CONF)
# print(CONF)

# Fourgy's sub-Commands


def anomtool_hash(p: ParamParser):
    "main function of anomtool-hash"
    name = p.last("source")
    hashTool = p.last("hash")
    for url in p.args["all"]:
        print(anomlib.pillow.hashValue(
            url, name=name, hashTool=hashTool))


def anomtool_do(p: ParamParser):
    "main function for 4g do"

    anomlib.builtin.do.do_repl(
        args=p.args["all"],
        history=p.last("history"),
        readline=p.last("readline"),
        prompt=p.last("prompt"),
        color=p.last("color"))


def anomtool_picload(p: ParamParser):
    "main function for anomtool picload"

    start = p.last("start")
    stop = p.last("stop")
    urlend = p.last("ending")
    ggType = p.last("type")
    ggHome = p.last("home")
    ggHome = os.path.expanduser(ggHome)
    for url_begin in p.args["all"]:
        anomlib.builtin.picload.getGallery(
            start, stop, url_begin, urlend,
            ggType=ggType, ggHome=ggHome,
        )
        # # print(getGallery(1, 90, "file-", ".jpeg"))


def main():
    "Main function of anomtool command"
    print(sys.argv[1:])
    print(CONF)
    p = ParamParser(pkg="anomlib", toml=CONF)
    # return 0

    match p.command:
        case "hash":
            anomtool_hash(p)
        case "picload":
            anomtool_picload(p)
        case "do":
            anomtool_do(p)
        # case "install":
        #     anomtool.foGive.install()


if __name__ == '__main__':
    sys.exit(main())
