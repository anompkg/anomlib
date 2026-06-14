"4g-with is a REPL command that allows calling commands in a loop while changing only args for it."

from pathlib import Path


import subprocess, re
import sys, tarfile, stat 
import hashlib, time


import logging, os, sys

import anomlib.shell
import anomlib.pillow

home = Path.home()

anomtoolDoCache = home / ".cache/anomtool/do"
anomtoolDoHistory = anomtoolDoCache / "history"
anomtoolDoLog = anomtoolDoCache / "do.log"


pillow.mkdirs(str(anomtoolDoCache))
pillow.mkdirs(str(anomtoolDoHistory))


# Configure logging

logging.basicConfig(filename=anomtoolDoLog, level=logging.DEBUG)

# Log messages


def inputline(
        color = "Yellow",
        prompt = "% ",
        history = "",
        readline = "rlwrap",
        args = sys.argv[1:]
    ):
    """Wrapper around readline tool (the rlwrap, a wrapper around gnu-readline in C)
    
    i can use any readline library when i figure out how to do it.
    Why so many wrappers? First make it work! Then make it beautiful!"""
    _history = history if history else " ".join(args)
    _history = anomtoolDoHistory / f"{_history}_history"
    return read_command(f"{readline} -p{color} -S '{prompt}' -H '{_history}' -o cat")


## Do will support params, but they needs to be added via --param=key=<value> or --param=flag, etc.
## each --param call will update params dictionary.

def do_repl(*args, **kwargs):
    command = " ".join(kwargs["args"])
    print("kwargs:", kwargs)
    "main function for 'anomtool do'"
    while True:
        cmd = inputline(**kwargs)
        print(cmd)
        if cmd == "exit":
            logging.debug(f"at-do: exiting command: {kwargs["args"]}")
            break
        elif not cmd:
            logging.debug(f'at-do: do nothing in this command: {kwargs["args"]}')
            # Do nothing if cmd is empty
            pass

        runcmd(f"{command} {cmd}")
        logging.debug(f'at-do: command: {command}  {cmd};')
