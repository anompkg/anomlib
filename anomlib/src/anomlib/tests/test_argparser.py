import pytest

import anomlib.argparser as sut  # Change to your module's import path


class FakeParser:
    """Small stand-in for anomlib.argparser.ArgParser."""

    def __init__(self, name, drafts=None):
        self.name = name
        self.drafts = drafts or {}
        self.parser = type("ParserState", (), {"prog": None})()

    def merge_parser_arguments(self, parser):
        pass

    def parse_args(self, args):
        # Enough to test ParamParser's argument flow:
        # treat every token as a positional argument.
        return {"args": list(args)}


@pytest.fixture
def parser_factory(monkeypatch):
    monkeypatch.setattr(sut, "ArgParser", FakeParser)
    return FakeParser


def make_parser_without_init(drafts, args, command="build"):
    """Create a ParamParser instance without loading TOML or parsing args."""
    parser = sut.ParamParser.__new__(sut.ParamParser)
    parser.drafts = drafts
    parser.command = command
    parser.args = {
        "original": list(args),
        "master": list(args),
        "command": [],
    }
    parser.options = {
        "master": {},
        "command": {},
    }
    parser.parsers = {
        "master": FakeParser("master", drafts=drafts),
    }
    return parser


# --- Helper function tests ---


def test_is_none_returns_true_for_none():
    assert sut.isNone(None) is True


@pytest.mark.parametrize("value", [0, False, "", [], "None"])
def test_is_none_returns_false_for_non_none_values(value):
    assert sut.isNone(value) is False


def test_interpret_arg_draft_combines_keys_and_shorts():
    draft = {
        "keys": ["--verbose"],
        "shorts": ["v"],
        "class": "flag",
        "help": "Increase verbosity",
    }

    result = sut.interpret_arg_draft(draft)

    assert result == (
        "flag",
        ["--verbose", "-v"],
        {"help": "Increase verbosity"},
    )


def test_interpret_arg_draft_uses_defaults():
    assert sut.interpret_arg_draft({"type": "string"}) == (
        "option",
        [],
        {"type": "string"},
    )


def test_interpret_arg_draft_mutates_input_current_behavior():
    """Documents current behavior: interpret_arg_draft pops fields in-place."""
    draft = {"shorts": ["x"], "keys": ["--example"]}

    sut.interpret_arg_draft(draft)

    assert "shorts" not in draft
    assert "keys" not in draft


def test_check_negatives_returns_values_after_last_false():
    assert sut.check_negatives([2, False, 3, False, 4]) == [4]


def test_check_negatives_returns_original_values_when_no_false():
    assert sut.check_negatives([1, 2, 3]) == [1, 2, 3]


def test_check_negatives_returns_empty_when_final_value_is_false():
    assert sut.check_negatives([1, False]) == []


def test_sum_flags_sums_values_after_last_false():
    assert sut.sum_flags([2, False, 3, 4]) == 7


def test_sum_flags_returns_zero_when_last_value_is_false():
    assert sut.sum_flags([2, False]) == 0


# --- Argument splitting tests ---


def test_split_args_finds_command_and_splits_arguments(parser_factory):
    drafts = {
        "master": {},
        "build": {},
    }
    parser = make_parser_without_init(
        drafts,
        ["--global", "build", "--local", "file.txt"],
    )

    parser._split_args_by("build")

    assert parser.command == "build"
    assert parser.args["master"] == ["--global"]
    assert parser.args["command"] == ["--local", "file.txt"]
    assert "build" in parser.parsers


def test_split_args_raises_if_command_is_repeated(parser_factory):
    drafts = {
        "master": {},
        "build": {},
    }
    parser = make_parser_without_init(
        drafts,
        ["build", "file.txt", "build"],
    )

    with pytest.raises(sut.KeywordOverflow):
        parser._split_args_by("build")


def test_split_args_raises_when_no_command_is_present(parser_factory):
    drafts = {
        "master": {},
        "build": {},
    }
    parser = make_parser_without_init(drafts, ["--global"])

    with pytest.raises(ValueError, match="Sub command is required"):
        parser.split_args()


def test_split_args_selects_first_command_in_drafts_order(parser_factory):
    """Documents current behavior; this may not match argument order."""
    drafts = {
        "master": {},
        "build": {},
        "clean": {},
    }
    parser = make_parser_without_init(
        drafts,
        ["clean", "build"],
    )

    parser.split_args()

    assert parser.command == "build"


# --- Parsing tests ---


def test_parse_args_master_uses_master_parser(parser_factory):
    drafts = {
        "master": {},
        "build": {},
    }
    parser = make_parser_without_init(drafts, ["--global"], command="build")
    parser.args["master"] = ["--global"]

    parser.parse_args("master")

    assert parser.parsers["master"].parser.prog == "anomtool"
    assert parser.args["master"] == ["--global"]


def test_parse_args_command_sets_command_program_name(parser_factory):
    drafts = {
        "master": {},
        "build": {},
    }
    parser = make_parser_without_init(drafts, ["--local"], command="build")
    parser.args["command"] = ["--local"]

    parser.parse_args()

    assert parser.parsers["build"].parser.prog == "anomtool build"
    assert parser.args["command"] == ["--local"]


# --- Flag merging tests ---


def test_fix_master_flags_merges_global_flag_count(parser_factory):
    drafts = {
        "master": {
            "--verbose": {"class": "flag"},
        },
        "build": {},
    }
    parser = make_parser_without_init(drafts, [], command="build")
    parser.options = {
        "master": {"--verbose": 2},
        "command": {"--verbose": 3},
        "all": {"--verbose": 5},
    }

    parser.fix_master_flags()

    assert parser.options["master"]["--verbose"] == 5
    assert parser.options["command"]["--verbose"] == 5
    assert parser.options["all"]["--verbose"] == 5


@pytest.mark.xfail(
    strict=False,
    reason="Known risk: fix_master_flags indexes a missing command option directly.",
)
def test_fix_master_flags_handles_missing_command_flag(parser_factory):
    drafts = {
        "master": {
            "--verbose": {"class": "flag"},
        },
        "build": {},
    }
    parser = make_parser_without_init(drafts, [], command="build")
    parser.options = {
        "master": {"--verbose": 2},
        "command": {},
        "all": {"--verbose": 2},
    }

    parser.fix_master_flags()

    assert parser.options["command"]["--verbose"] == 2


# --- last() tests ---


def test_last_returns_last_value_for_list_option():
    drafts = {
        "master": {},
        "build": {
            "--output": {"type": "string"},
        },
    }
    parser = make_parser_without_init(drafts, [], command="build")
    parser.options["all"] = {"--output": ["first.txt", "last.txt"]}

    assert parser.last("--output") == "last.txt"


def test_last_returns_type_default_for_empty_list():
    drafts = {
        "master": {},
        "build": {
            "--count": {"type": "int"},
        },
    }
    parser = make_parser_without_init(drafts, [], command="build")
    parser.options["all"] = {"--count": []}

    # This test assumes "int" is supported by the module's type mapping.
    if "int" not in sut.argparser.TYPE_NAMES:
        pytest.skip("'int' is not present in argparser.TYPE_NAMES")

    assert parser.last("--count") == sut.argparser.TYPE_NAMES["int"]()


@pytest.mark.xfail(
    strict=False,
    reason="Known risk: last() indexes the requested option directly.",
)
def test_last_unknown_option_has_clear_error():
    drafts = {"master": {}, "build": {}}
    parser = make_parser_without_init(drafts, [], command="build")
    parser.options["all"] = {}

    with pytest.raises((KeyError, ValueError), match="unknown|Unknown|missing|Missing"):
        parser.last("--missing")


@pytest.mark.xfail(
    strict=False,
    reason="Known risk: last() expects a list-like value and uses items[-1].",
)
def test_last_accepts_scalar_option_value():
    drafts = {
        "master": {},
        "build": {
            "--count": {"type": "int"},
        },
    }
    parser = make_parser_without_init(drafts, [], command="build")
    parser.options["all"] = {"--count": 3}

    assert parser.last("--count") == 3
