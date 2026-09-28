"Arglib is a fork of paramparser but uses toml format and is more simplified"

import logging
import optparse
import sys
import textwrap
from collections.abc import Iterable
from pprint import pprint

from anomlib import confman
from anomlib import argparser
from anomlib.argparser import ArgParser

from importlib.resources import files

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

    def __init__(self, toml="params/anomtool.toml",
                 pkg="anomlib", args=sys.argv[1:]):
        # Remember which pkg delivers built-in configs
        # Select pkg as source of configs
        self.pkg = pkg
        # Default sub-command
        self.command = "help"
        self.toml = toml
        # Correct way - files is a function
        self.toml = files(pkg).joinpath(toml)
        # config_text = config_files.read_text()
        # config = tomllib.loads(config_text)
        # print(config)

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

        # Load all rules that describe how to parse args
        self.drafts = confman.Conflock(self.toml).load()

        # Prepare master namespace
        self.parsers = {'master': ArgParser("master", drafts=self.drafts)}
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

        # Fix Global Flags Counter
        self.fix_master_flags()

    def fix_master_flags(self):
        """Fix global flags that went into local namespace.
        If local object redefined the flag, it is ignored.
        Fix only affects master flags that were not redefined."""

        # Fix global flag counters
        for key, global_value in self.options["master"].items():

            cmd = self.drafts[self.command]
            main = self.drafts["master"][key]
            # Make sure that we deal with "flag" class only (not "value" class)
            if key not in cmd and main["class"] == "flag":
                # TODO: Cmds in drafts no longer have
                #       params split by options and flags.
                # TODO: Add get_global_options() and get_command_options()

                # quick aliases to current parsed options
                value = self.options["command"][key]

                # Clear count if -no or -non was used in command namespace
                values = [global_value, value]
                total = sum_flags(values)

                # Apply merged count
                self.options["command"][key] = total
                self.options["master"][key] = total
                self.options["all"][key] = total

    def _split_args_by(self, keyword):
        "Split args by command as keyword"
        if keyword in self.args["original"] and keyword != "master":
            self.command = keyword

            self.parsers[keyword] = ArgParser(keyword, drafts=self.drafts)
            self.parsers[keyword].merge_parser_arguments(self.parsers["master"].parser)

            index = self.args["original"].index(keyword)
            # split arguments by command so we can parse before args and after args.
            # End params are linked to the command, when params before are more global.
            self.args["master"] = self.args["original"][:index]
            self.args["command"] = self.args["original"][index+1:]
            # Merge options, but command's options will be marked as command's sub
            # vars(parse(self._args[1]));    {command}.{option} * vars(parse(self._args[2]))

    def split_args(self):
        "Split args into namespaces"
        # Usage: 4g <options> <command> <command.options> <args>
        for cmd in self.drafts:
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

        if command not in self.parsers:
            self.parsers[command] = ArgParser(command, drafts=self.drafts)
            self.parsers[command].merge_parser_arguments(self.parsers[command].parser)

        parser = self.parsers[command]
        parser.prog = f"anomtool {command}"

        match command:
            case "master":
                # Only master's progname is an exception
                parser.prog = "anomtool"
            # case "help":
            #     parser.print_help()
            # TODO: after switching to argparse, print_help not working atm

        # Note: opts["args"] has the rest of arguments
        opts = parser.parse_args(self.args[namespace])
        args = opts.pop("args", [])

        self.options[namespace] |= opts
        self.args[namespace] = args

    def last(self, name, area="all"):
        """Get last option or empty string.
        ATM it returns empty string, but
        later it will return object according to type.

        name: option name
        area: master|command|all
        default: should be the type that option uses"""
        default = self.drafts[self.command][name].get("type", "string")

        default = argparser.TYPE_NAMES[default]()

        items = self.options[area][name]
        # Return last item or empty default
        return items[-1] if items else default


# p = ParamParser()

# print(p.command)
# print(p.args)
# print(p.options)
