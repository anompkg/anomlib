"4g-with is a REPL command that allows calling commands in a loop while changing only args for it."

from pathlib import Path


import subprocess, re
import sys, tarfile, stat 
import hashlib, time


import logging, os, sys


# Diff Status Codes
SAME = 0
DIFFERENT = 1
TROUBLE = 2

def runcmd(command):
    with subprocess.Popen(command, shell=True) as process:
        process.communicate()


def execute_command(command):
    """
        Execute a command and return output, errors and status code.  
    """
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    # Output, Errors, Exit/Status Code
    return {
        "output": stdout.decode().rstrip(),
        "errors": stderr.decode().rstrip(),
        "status": process.returncode,
        "command": command
        }

def run_command(command):
    """
        Execute a command and return output, errors and status code.  
    """
    started = time.time()
    result = execute_command(command)
    ended = time.time()
    
    result["time"] = ended-started

    return result

def read_command(command, errors=[""], status=[0]):
    """Run Command and return just output.
    
    By default it expects no errors.
    
    if errors and status params are not None, values will get asserted for testing.
    
    If errors and/or status in params are set None, they will get omitted.
    
    It is allowed to have multiple acceptable statuses. e.g. diff returns 0 and 1 and it is fine
    
    @param: status List of Acceptable Exit Codes.    
    """
    result = execute_command(command)
    
    command_info = f"""Command: {result['command']}
Status Code: {result['status']}
Errors:    
{result['errors']}
[End Of Errors]
"""
    
    # Test errors according to preferences set in params
    if status is not None:
        assert result["status"] in status, command_info
    
    if errors is not None:
        assert result["errors"] in errors, command_info

    assert "output" in result, command_info
    
    # We only need output
    return result["output"]


home = Path.home()

anomtoolDoCache = home / ".cache/anomtool/do"
anomtoolDoHistory = anomtoolDoCache / "history"
anomtoolDoLog = anomtoolDoCache / "do.log"

def mkdirs(path):
    if not os.path.exists(anomtoolDoCache):
        os.makedirs(str(anomtoolDoCache))

mkdirs(str(anomtoolDoCache))
mkdirs(str(anomtoolDoHistory))


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
