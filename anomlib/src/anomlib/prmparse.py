"Arglib is a fork of paramparser but uses toml format and is more simplified"

import logging
import optparse
import sys
import textwrap
from collections.abc import Iterable
from pprint import pprint

import confman
from argparser import ArgParser

# DATA = confman.Conflock("params/anomtool.toml").load()


def isNone(value):
    "Check if value is None"
    return isinstance(value, type(None))


def interpret_arg_draft(draft):
    shorts = list(draft.pop("shorts")) if "shorts" in draft else []
    keys = draft.pop("keys") if "keys" in draft else []
    keys += ['-' + e for e in shorts]
    cls = draft.pop("class") if "class" in draft else "option"

    # return args with kwargs
    return cls, keys, draft


def interpret_cmd_draft(draft):
    for subs in draft.values():
        for param in subs.values():
            print(interpret_arg_draft(param))


def check_negatives(values: Iterable[int | None | bool]) -> list[int | None | bool]:
    values = list(values)

    for index in range(len(values) - 1, -1, -1):
        if values[index] is False:
            return values[index + 1:]

    return values


def sum_flags(values: Iterable[int | None | bool]) -> int:
    return sum(value or 0 for value in check_negatives(values))


class ParamParser:
    """Wrapper around optparse supports toml.
    Hybrid Param Parser.
    This is a test command.
    Report
 bugs to https://codeberg.org/tfed/anomlib/issues.
    """

    def __init__(self, toml="params/anomtool.toml", args=sys.argv[1:]):
        # Default sub-command
        self.command = "help"

        # Raw Arguments
        self.args = {
            # All original Arguments
            'original': args,
            # Global Arguments (Options Mostly)
            # default: = all args, otherwise only up to first keyword
            'master': args,
            # Command's Options with Arguments
            'command': []
        }
        
        # Namespaces with Options
        self.options = {
            'master': {},
            'command': {}
        }

        self.commands = confman.Conflock(toml).load()

        # Prepare master namespace
        self.parsers = {'master': ArgParser("master", drafts=DATA)}
        # TODO: after finding out if sub command was used.
        #   if so we should make another parser for it.
        self.init()
        
    def init(self):
        # Split arguments in master and command's areas 
        self.split_args()

        # Parse args and options
        self.parse_args("master")
        self.parse_args()
        
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
                values = [global_value, value]
                total = sum_flags(values)

                # Debug
                print(values)

                # Apply merged count
                self.options["command"][key] = total
                self.options["master"][key] = total
                self.options["all"][key] = total

    def _split_args_by(self, keyword):
        if keyword in self.args["original"]:
            self.command = keyword

            index = self.args["original"].index(keyword)
            # split arguments by command so we can parse before args and after args.
            # End params are linked to the command, when params before are more global.
            self.args["master"] = self.args["original"][:index]
            self.args["command"] = self.args["original"][index+1:]
            # Merge options, but command's options will be marked as command's sub
            # vars(parse(self._args[1]));    {command}.{option} * vars(parse(self._args[2]))

    def split_args(self):
        # Usage: 4g <options> <command> <command.options> <args>
        for cmd in self.commands:
            if cmd in self.args["original"] and cmd != "master":
                self._split_args_by(cmd)
                break
        else:
            # Otherwise if there is no cmd inside we can just drop help msg
            # And exit with help error
            sys.exit(2)

    def parse_args(self, command=None):
        command = command or self.command

        # Namespace is either command or master
        namespace = "master" if command == "master" else "command"


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


p = ParamParser()

print(p.command)
