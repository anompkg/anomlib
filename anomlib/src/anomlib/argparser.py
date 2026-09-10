"""Parse command line arguments.

Sub commands are supported by arglib.
Nested sub commands for arglib are not planned yet."""

# Note: This code was vibe-coded as i got bored
# I had paramparser that worked, but dont wanna play parsing anymore
# I promise i will replace these vibes with blood, sweat and tears

import argparse
import confman

DATA = confman.Conflock("params/anomtool.toml").load()


# Compatibility with optparse-style type names.
TYPE_NAMES = {
    "string": str,
    "int": int,
    "integer": int,
    "float": float,
}

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
    ""
    def __init__(self, command, drafts=None, parser=None):
        self.command = command
        self.drafts = DRAFTS if drafts is None else drafts
        self.parser = (
            parser
            if parser is not None
            else argparse.ArgumentParser()
        )

    def build(self):
        try:
            params = self.drafts[self.command]
            # Support all args
            params["args"] = ARGS
        except KeyError:
            raise ValueError(
                f"Unknown command: {self.command!r}"
            )

        for name, config in params.items():
            self.add_option(name, config)

        return self

    def add_option(self, name, params):
        """
        Dispatch an option or positional argument to its handler.

        Supported classes:

            "flag"   Boolean option
            "value"  Option that accepts a value
            "arg"    Positional argument
        """
        params = dict(params)
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
        params = dict(params)

        shorts = params.pop("shorts", "")
        keys = params.pop("keys", [])
        dest = params.setdefault("dest", name)

        positive_params = dict(params)
        positive_params.update({
            "action": "store_true",
            "dest": dest,
        })

        self._add_option_argument(
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

        self._convert_type(params)

        return self._add_option_argument(
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

    def _add_option_argument(
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
        callables accepted by argparse.
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


def test_argparser(command, *args, **kwargs):
    parser = ArgParser(command, *args, **kwargs).build()
    values = parser.parse_args()

    print(values)


if __name__ == "__main__":
    # test_argparser("diff")
    test_argparser("do", drafts=DATA)
