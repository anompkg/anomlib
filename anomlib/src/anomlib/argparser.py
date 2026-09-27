"""Parse command line arguments.

Sub commands are supported by arglib.
Nested sub commands for arglib are not planned yet."""

# Note: This code was vibe-coded as i got bored
# I had paramparser that worked, but dont wanna play parsing anymore
# I promise i will replace these vibes with blood, sweat and tears
import argparse
import tomlkit
import anomlib.confman


# Compatibility with optparse-style type names.
TYPE_NAMES = {
    "string": str,
    "int": int,
    "integer": int,
    "float": float,
    "bool": bool,
}

FLAG_TYPES = (int, bool, float, list, tomlkit.items.Array)


# Default structure to support arguments
ARGS = {
    "class": "arg",
    "nargs": "*",
    "type": "string",
    "help": "Input files and other positional arguments",
}

DRAFTS = {
    "diff": {
        "patch": {
            "class": "flag",
            "shorts": "pu",
            "help": "Generate patch",
            "default": True,
        },
        "output": {
            "class": "value",
            "shorts": "o",
            "keys": ["file"],
            "type": "string",
            "help": "Write output to a file",
        }
    },
}


class ArgParser:
    "ArgParser handles one sub command"
    def __init__(self, command, drafts=None, parser=None):
        self.command = command
        self.drafts = DRAFTS if drafts is None else drafts
        self.parser = (
            parser
            if parser is not None
            else argparse.ArgumentParser()
        )
        self.build()

    def build(self):
        try:
            self.params = self.drafts[self.command]
            # Support all args
            self.params["args"] = ARGS
        except KeyError:
            print(self.drafts)
            raise ValueError(
                f"Unknown command: {self.command!r}"
            )

        for name, config in self.params.items():
            self.add_param(name, config)

        return self

    def add_param(self, name, params):
        """
        Dispatch an option or positional argument to its handler.

        Supported classes:

            "flag"   Boolean option
            "value"  Option that accepts a value
            "arg"    Positional argument
        """
        params = dict(params)
        # "value" is default class
        option_class = params.pop("class", "value")

        handler = getattr(
            self,
            f"add_{option_class}",
            None,
        )

        if handler is None:
            raise ValueError(
                f"Unsupported option class: {option_class!r}"
            )

        return handler(name, params)

    def add_flag(self, name, params):
        """
        Add a Boolean option and its negative aliases.

        Example:

            --patch
            --no-patch
            --non-patch
        """

        # FIx flags, they cant have values
        params.pop("default", None)
        params.pop("type", None)

        params = dict(params)

        shorts = params.pop("shorts", "")
        keys = params.pop("keys", [])

        dest = params.setdefault("dest", name)

        positive_params = dict(params)
        positive_params.update({
            "action": "count",
            "dest": dest,
        })

        self._add_option(
            name=name,
            shorts=shorts,
            keys=keys,
            params=positive_params,
        )

        # SUPPRESS prevents the negative option from replacing the
        # default defined by the positive option.
        self.parser.add_argument(
            f"--no-{name}",
            f"--non-{name}",
            action="store_false",
            dest=dest,
            default=argparse.SUPPRESS,
        )

        return self

    def add_value(self, name, params):
        """
        Add an option that accepts a value.

        Example:

            --output changes.diff
            -o changes.diff
        """
        params = dict(params)

        shorts = params.pop("shorts", "")
        keys = params.pop("keys", [])

        # TODO: Allow repeating options
        params["action"] = "append"
        params["default"] = []

        self._convert_type(params)

        return self._add_option(
            name=name,
            shorts=shorts,
            keys=keys,
            params=params,
        )

    def add_arg(self, name, params):
        """
        Add a positional argument.

        Example configuration:

            "args": {
                "class": "arg",
                "nargs": "*",
            }

        This allows:

            program file1.txt --output result.diff file2.txt
        """
        params = dict(params)

        # These settings apply to options, not positional arguments.
        params.pop("shorts", None)
        params.pop("keys", None)

        self._convert_type(params)

        self.parser.add_argument(
            name,
            **params,
        )

        return self

    def _add_option(
        self,
        name,
        shorts="",
        keys=None,
        params=None,
    ):
        """
        Add an optional argument with short and long aliases.

        A string such as "pu" becomes:

            -p
            -u
        """
        keys = [] if keys is None else keys
        params = {} if params is None else params

        option_strings = [
            *(f"-{short}" for short in shorts),
            f"--{name}",
            *(
                key if key.startswith("-") else f"--{key}"
                for key in keys
            ),
        ]

        self.parser.add_argument(
            *option_strings,
            **params,
        )

        return self

    @staticmethod
    def _convert_type(params):
        """
        Convert type names such as "string" and "int" into
        callables accepted by argparser.
        """
        value_type = params.get("type")

        if not isinstance(value_type, str):
            return

        try:
            params["type"] = TYPE_NAMES[value_type]
        except KeyError:
            raise ValueError(
                f"Unsupported option type: {value_type!r}"
            )

    def parse_args(self, args=None):
        """
        Parse options and interspersed positional arguments.

        Unlike regular parse_args(), parse_intermixed_args() allows
        positional arguments to appear before, between, and after
        optional arguments.
        """
        try:
            namespace = self.parser.parse_intermixed_args(args)
        except AttributeError:
            raise RuntimeError(
                "Intermixed argument parsing requires Python 3.7 "
                "or newer."
            )

        return vars(namespace)

    def merge_parser_arguments(self, source):
        """Add arguments from source to target unless target already defines them."""

        target_dests = {
            action.dest
            for action in self.parser._actions
            if action.dest != "help"
        }

        target_options = {
            option
            for action in self.parser._actions
            for option in action.option_strings
        }

        for action in source._actions:
            if action.dest == "help":
                continue

            # A has redefined this argument
            if action.dest in target_dests:
                continue

            # Avoid option-string collisions too
            if any(option in target_options for option in action.option_strings):
                continue

            self.parser._add_action(action)

            target_dests.add(action.dest)
            target_options.update(action.option_strings)


def test_argparser(command, *args, **kwargs):
    parser = ArgParser(command, *args, **kwargs)

    # values = parser.parse_args(["1", "-s", "foo", "bye"])
    # print(values)

    values = parser.parse_args()
    print(values)


if __name__ == "__main__":
    test_argparser("diff")
    # DATA = anomlib.confman.Conflock("params/anomtool.toml").load()
    # test_argparser("pull", drafts=DATA)
    # test_argparser("master", drafts=DATA)
