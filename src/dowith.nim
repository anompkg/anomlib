from std/cmdline import commandLineParams
from std/osproc import startProcess, ProcessOption, waitForExit, close, execProcess
#from std/os import fileExists

proc runCommand*(command: string, args: openArray[string]): int =
  ## This will run a command with the given args and return its exit code upon completion
  let process = startProcess(command, args=args, options={poParentStreams})
  result = process.waitForExit()
  process.close()

discard runCommand("/usr/bin/mkdir", args=["-p", "~/.local/log"])

# execProc( )
var log = "$HOME/.local/log/.dowith.log"

proc input(line*:string, promt="% "): bool =
  # Default promt is "% "
  stdout.write promt
  
  # Ask Users commands in real time 
  stdin.readLine(line)

proc dowith(commandName="/bin/echo", args:seq[string], promt="% "): int =
  var line: string, params = args

  # Ask Users commands in real time 
  while input(line, promt):

    # Don't add line in args, if empty
    if line != "":
      params.add(line)

    # Run sub-command
    result = runCommand(commandName, args=params)

    # Reset arguments
    params = args


var
  cmdName = commandLineParams()[0]
  args = commandLineParams()[1 .. ^1]

discard dowith(cmdName, args)


