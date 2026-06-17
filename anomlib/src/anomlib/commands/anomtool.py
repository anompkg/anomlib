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

import logging
import sys
import textwrap
import optparse
# import os
# import argparse
# import subprocess
# import getopt
# import argparse
# import sys

#import anomtool.foGet
import anomlib.builtin.do
#import anomtool.foGive
import anomlib.params.anomtool
from anomlib.paramparser import ParamParser
import anomlib.pillow
import anomlib.builtin.picload


## Forgy's sub-Commands

def anomtool_hash(p:ParamParser):
    "main function of anomtool-hash"
    name = p.options["all"]["source"]
    hashTool = p.options["all"]["hash"]
    for url in p.args["all"]:
        print(anomlib.pillow.hashForgySource(url, name=name, hashTool=hashTool))



def anomtool_do(p:ParamParser):
    "main function for 4g do"

    anomlib.builtin.do.do_repl(
        args = p.args["all"],
        history = p.options["all"]["history"],
        readline = p.options["all"]["readline"],
        prompt = p.options["all"]["prompt"],
        color = p.options["all"]["color"])

# def anomtool_pull(p:ParamParser):
#     "main function for 4g pull"

#     for url in p.args["all"]:
#         days = p.options["all"]["days"]
#         hours = p.options["all"]["hours"]
#         anomtool.foGive.pull(url, days=days, hours=hours)


def main():
    p = ParamParser(commands=anomlib.params.anomtool.commands)

    match p.command:
        case "hash":
            anomtool_hash(p)
        case "picload":
            pass
        case "do":
            anomtool_do(p)
        # case "install":
        #     anomtool.foGive.install()

if __name__ == '__main__':
	sys.exit(main())
