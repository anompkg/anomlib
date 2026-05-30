from std/cmdline import commandLineParams
from std/osproc import startProcess, waitForExit, close, ProcessOption


proc runCommand*(command: string, args: openArray[string]): int =
  ## This will run a command with the given args and return its exit code upon completion
  let process = startProcess(command, args=args, options={poParentStreams})
  result = process.waitForExit()
  process.close()


proc input(line: var string, promt="% "): bool =
  # Default promt is "% "
  stdout.write promt

  # Ask Users commands in real time
  stdin.readLine(line)


proc dowith(commandName="/bin/echo", args:seq[string], promt="% "): int =
  var line: string

  # Ask Users commands in real time
  while input(line, promt):

    # Run Interpreter in loop
    case line
      # Run base command:
      of "": result = runCommand(commandName, args=args)
      # exit command
      of "exit": return 0
      # Run sub-command
      else: result = runCommand(commandName, args=args & line)


# Take arguments and script's name separate
var
  cmdName = commandLineParams()[0]
  args = commandLineParams()[1 .. ^1]


# Run dowith with base command, and base args in interactive mode
discard dowith(cmdName, args)

