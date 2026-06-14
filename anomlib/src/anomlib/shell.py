
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

