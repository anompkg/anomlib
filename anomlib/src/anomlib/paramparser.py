#!/usr/bin/env python3

import logging
import sys
import textwrap
import optparse

def isNone(value):
    "Check if value is None"
    return isinstance(value, type(None))

class ParamParser:
    """Wrapper around optparse.
    Hybrid Param Parser.
    """
    def _new_parser(self):
        return optparse.OptionParser(epilog=textwrap.dedent("""\
    This is a test command.
    
    Report bugs to https://codeberg.org/tfed/anomlib/issues."""))

    def __init__(self, args=sys.argv[1:], commands={}):
        self.command = "help"
        
        ## Raw Arguments
        self.args = {
            # All original Arguments
            'original': args,
            # Global Arguments (Options Mostly)
            # default: = all args, otherwise only up to first keyword
            'master': args,
            # Command's Options with Arguments 
            'command': []
        }
        
        ## Options
        self.options = {
            'master': {},
            'command': {}
        }

        self.commands = commands

        ## Parsers
        # Global and Command Parsers
        self.parsers = {'master': self._new_parser()}
        # the rest of parsers        
        for cmd in self.commands:
            self.parsers[cmd] = self._new_parser()

        self.init()

    def get_flag_safely(self, namespace, key):

        # Return 0 if value does not exist
        if namespace not in self.options or key not in self.options[namespace]:
            return 0

        # Otherwise, Return flag counter
        return self.options[namespace][key]
        
    def init(self):
        # Split arguments in master and command's areas 
        self.splitArgs()

        # Parse args and options
        self.parseArgs("master")
        self.parseArgs()
        
        # Allow skipping areas while processing.
        self.args["all"] = self.args["master"] + self.args["command"]
        self.options["all"] = self.options["master"] | self.options["command"]
        
        # Debug
        print()
        print()

        # Fix Global Flags Counter
        self.fix_master_flags()
        
        # Debug
        print("Arguments:")
        for key in self.options["master"]:
            print(f"{key} args: ")

        print("Arguments:")
        for key, value in self.args.items():
            print(f"{key} args: ", value)

        print("Options:")
        for key, value in self.options.items():
            print(f"{key} options: ", value)

        print()

    def fix_master_flags(self):

        # Fix global flag counters
        for key, value in self.options["command"].items():

            if key in self.options["master"]:
                # Debug
                print(f'{key} is a common flag')

                # quick aliases to the parser's configured options
                global_options = self.commands["master"]["options"]
                command_options = self.commands[self.command]["options"]
                # quick aliases to current parsed options
                global_value = self.options["master"][key]
                

                # Make sure that we deal with "flag options" only (not "option options")
                if key in global_options or key in command_options:
                    print(f"{key} is not a flag but an option")
                    # Skip if option
                    continue

                # Debug
                print(f"{key} flag")
                
                # Clear count if -no or -non was used in command namespace
                if False in [global_value, value]:
                    global_value = 0
                
                # Convert None and False values to 0 while getting counts of --verboses
                values = [global_value, value]
                # Reset value to 0 when None
                values = [[value, 0][isNone(value)] for value in values]

                # Debug
                print(values)

                # Update summarized result
                result = sum(values)

                # Apply merged count
                self.options["command"][key] = result
                self.options["master"][key] = result
                self.options["all"][key] = result

    def _splitArgsByKeyword(self, keyword):
        if keyword in self.args["original"]:
            self.command = keyword

            index = self.args["original"].index(keyword)
            # split arguments by command so we can parse before args and after args.
            # End params are linked to the command, when params before are more global.
            self.args["master"] = self.args["original"][:index]
            self.args["command"] = self.args["original"][index+1:]
            # Merge options, but command's options will be marked as command's sub
            # vars(parse(self._args[1]));    {command}.{option} * vars(parse(self._args[2]))

    def splitArgs(self):
        # Usage: 4g <options> <command> <command.options> <args>
        for cmd in self.commands:
            if cmd in sys.argv[1:] and cmd != "master":
                self._splitArgsByKeyword(cmd)
                break
        else:
            # Otherwise if there is no cmd inside we can just drop help msg
            # And exit with help error
            sys.exit(2)

    def add_flag(self, parser, dest, *args, **kwargs):
        parser.add_option(f'--{dest}', *args, dest=dest, action='count', **kwargs)

        # Support --no- with --non- key prefixes to set keys False
        parser.add_option(f"--no-{dest}", dest=dest, action='store_false')
        parser.add_option(f"--non-{dest}", dest=dest, action='store_false')

    def add_flags(self, parser, command):
        if "flags" not in self.commands[command]:
            self.commands[command]["flags"] = {}

        flags = self.commands[command]["flags"]

        for dest, act in flags.items():
            print(f'{command}: {dest}: {act}')
            (args, kwargs) = act['args'], act['kwargs']
            self.add_flag(parser, dest, *args, **kwargs)

        ## Warning: Recursion:
        # We want to allow global arguments into command namespace as well
        if command != "master":
            self.add_flags(parser, "master")

    def add_options(self, parser, command):
        if "options" not in self.commands[command]:
            self.commands[command]["options"] = {}

        options = self.commands[command]["options"]

        for dest, opt in options.items():
            print(f'{command}: {dest}: {opt}')
            (args, kwargs) = opt['args'], opt['kwargs']
            parser.add_option(f"--{dest}", *args, **kwargs)

        ## Warning: Recursion:
        # Allow master arguments working inside command's namespace
        if command != "master":
            self.add_options(parser, "master")

    def parseArgs(self, command=None):
        if not command:
            command = self.command
        
        # Namespace is either command or master
        namespace = ["command", "master"][command == "master"]
        
        if namespace == "command":
            assert self.options[namespace] == {}

        parser = self.parsers[command]
        parser.prog = f"4g {command}"
        
        self.add_options(parser, command)
        self.add_flags(parser, command)
        match command:
            case "master":
                # Only master's progname is an exception 
                parser.prog = "4g"
            case "help":
                parser.print_help()


        opts, urls = parser.parse_args(self.args[namespace])
        opts = vars(opts)
        
        self.options[namespace] |= opts
        self.args[namespace] = urls
