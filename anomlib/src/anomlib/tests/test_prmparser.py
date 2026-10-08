import pytest

from anomlib import prmparser as sut


def make_parser(*, drafts=None, command="build", args=None, options=None):
    """Create a ParamParser without loading TOML or invoking ArgParser."""
    parser = sut.ParamParser.__new__(sut.ParamParser)
    parser.command = command
    parser.drafts = drafts or {
        "master": {},
        command: {},
    }
    parser.args = args or {
        "original": [],
        "master": [],
        "command": [],
    }
    parser.options = options or {
        "master": {},
        "command": {},
        "all": {},
    }
    parser.parsers = {}
    return parser


# --- Small helper functions ---


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ([], []),
        ([1, 2, 3], [1, 2, 3]),
        ([1, False, 3], [3]),
        ([1, False], []),
        ([2, False, 3, False, 4], [4]),
    ],
)
def test_check_negatives(values, expected):
    assert sut.check_negatives(values) == expected


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ([], 0),
        ([1, 2, 3], 6),
        ([1, False, 3], 3),
        ([2, False, 3, False, 4], 4),
    ],
)
def test_sum_flags(values, expected):
    assert sut.sum_flags(values) == expected


def test_interpret_arg_draft():
    draft = {
        "keys": ["--verbose"],
        "shorts": ["v"],
        "class": "flag",
        "help": "Increase verbosity",
    }

    assert sut.interpret_arg_draft(draft) == (
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


def test_interpret_arg_draft_mutates_the_draft():
    """Captures the current pop()-based behavior."""
    draft = {"keys": ["--name"], "class": "option"}

    sut.interpret_arg_draft(draft)

    assert draft == {}


# --- Argument splitting ---


class FakeArgParser:
    def __init__(self, name, drafts=None):
        self.name = name
        self.drafts = drafts
        self.parser = type("ParserState", (), {"prog": None})()

    def merge_parser_arguments(self, parser):
        pass

    def parse_args(self, args):
        return {"args": list(args)}


@pytest.fixture
def fake_argparser(monkeypatch):
    monkeypatch.setattr(sut, "ArgParser", FakeArgParser)


def test_split_args_by_command(fake_argparser):
    parser = make_parser(
        drafts={"master": {}, "build": {}},
        args={
            "original": ["--global", "build", "--local", "file.txt"],
            "master": ["--global", "build", "--local", "file.txt"],
            "command": [],
        },
    )
    parser.parsers = {"master": FakeArgParser("master")}

    parser._split_args_by("build")

    assert parser.command == "build"
    assert parser.args["master"] == ["--global"]
    assert parser.args["command"] == ["--local", "file.txt"]
    assert "build" in parser.parsers


def test_split_args_by_raises_if_command_occurs_more_than_once(fake_argparser):
    parser = make_parser(
        drafts={"master": {}, "build": {}},
        args={
            "original": ["build", "file.txt", "build"],
            "master": ["build", "file.txt", "build"],
            "command": [],
        },
    )
    parser.parsers = {"master": FakeArgParser("master")}

    with pytest.raises(sut.KeywordOverflow):
        parser._split_args_by("build")


def test_split_args_requires_a_subcommand(fake_argparser):
    parser = make_parser(
        drafts={"master": {}, "build": {}},
        args={
            "original": ["--verbose"],
            "master": ["--verbose"],
            "command": [],
        },
    )

    with pytest.raises(ValueError, match="Sub command is required"):
        parser.split_args()


def test_split_args_uses_draft_order_not_argument_order(fake_argparser):
    """Documents current behavior; it may be worth changing."""
    parser = make_parser(
        drafts={"master": {}, "build": {}, "clean": {}},
        args={
            "original": ["clean", "build"],
            "master": ["clean", "build"],
            "command": [],
        },
    )
    parser.parsers = {"master": FakeArgParser("master")}

    parser.split_args()

    assert parser.command == "build"


# --- Argument parsing ---


def test_parse_args_sets_master_program_name(fake_argparser):
    parser = make_parser(
        drafts={"master": {}, "build": {}},
        command="build",
        args={
            "original": ["--verbose"],
            "master": ["--verbose"],
            "command": [],
        },
    )
    parser.parsers = {"master": FakeArgParser("master")}

    parser.parse_args("master")

    assert parser.parsers["master"].parser.prog == "anomtool"
    assert parser.args["master"] == ["--verbose"]


def test_parse_args_sets_command_program_name(fake_argparser):
    parser = make_parser(
        drafts={"master": {}, "build": {}},
        command="build",
        args={
            "original": ["build", "--output", "file.txt"],
            "master": [],
            "command": ["--output", "file.txt"],
        },
    )
    parser.parsers = {"master": FakeArgParser("master")}

    parser.parse_args()

    assert parser.parsers["build"].parser.prog == "anomtool build"
    assert parser.args["command"] == ["--output", "file.txt"]


def test_parse_args_rejects_nonempty_command_options(fake_argparser):
    parser = make_parser(
        drafts={"master": {}, "build": {}},
        command="build",
        args={"original": [], "master": [], "command": []},
        options={"master": {}, "command": {"--old": True}, "all": {}},
    )
    parser.parsers = {"master": FakeArgParser("master")}

    with pytest.raises(AssertionError):
        parser.parse_args()


# --- Global flag merging ---


def test_fix_master_flags_combines_global_and_command_counts(fake_argparser):
    parser = make_parser(
        drafts={
            "master": {"--verbose": {"class": "flag"}},
            "build": {},
        },
        command="build",
        options={
            "master": {"--verbose": 2},
            "command": {"--verbose": 3},
            "all": {"--verbose": 3},
        },
    )

    parser.fix_master_flags()

    assert parser.options["master"]["--verbose"] == 5
    assert parser.options["command"]["--verbose"] == 5
    assert parser.options["all"]["--verbose"] == 5


def test_fix_master_flags_does_not_merge_a_command_override(fake_argparser):
    parser = make_parser(
        drafts={
            "master": {"--verbose": {"class": "flag"}},
            "build": {"--verbose": {"class": "option"}},
        },
        command="build",
        options={
            "master": {"--verbose": 2},
            "command": {"--verbose": 3},
            "all": {"--verbose": 3},
        },
    )

    parser.fix_master_flags()

    assert parser.options["master"]["--verbose"] == 2
    assert parser.options["command"]["--verbose"] == 3
    assert parser.options["all"]["--verbose"] == 3


@pytest.mark.xfail(
    strict=False,
    reason="Current implementation indexes a missing command option directly.",
)
def test_fix_master_flags_handles_missing_command_flag(fake_argparser):
    parser = make_parser(
        drafts={
            "master": {"--verbose": {"class": "flag"}},
            "build": {},
        },
        command="build",
        options={
            "master": {"--verbose": 2},
            "command": {},
            "all": {"--verbose": 2},
        },
    )

    parser.fix_master_flags()

    assert parser.options["command"]["--verbose"] == 2


# --- The second, effective last() implementation ---


def test_last_returns_scalar_value():
    parser = make_parser(
        drafts={
            "master": {},
            "build": {"--count": {"type": "int"}},
        },
        options={
            "master": {},
            "command": {"--count": 3},
            "all": {"--count": 3},
        },
    )

    assert parser.last("--count") == 3


def test_last_returns_last_item_of_list():
    parser = make_parser(
        drafts={
            "master": {},
            "build": {"--name": {"type": "string"}},
        },
        options={
            "master": {},
            "command": {"--name": ["first", "last"]},
            "all": {"--name": ["first", "last"]},
        },
    )

    assert parser.last("--name") == "last"


def test_last_returns_draft_default_when_option_was_not_parsed():
    parser = make_parser(
        drafts={
            "master": {},
            "build": {"--output": {"default": "result.txt"}},
        },
        options={"master": {}, "command": {}, "all": {}},
    )

    assert parser.last("--output") == "result.txt"


def test_last_returns_none_when_no_value_or_draft_default_exists():
    parser = make_parser(
        drafts={"master": {}, "build": {"--output": {}}},
        options={"master": {}, "command": {}, "all": {}},
    )

    assert parser.last("--output") is None


def test_last_uses_explicit_default():
    parser = make_parser(
        drafts={"master": {}, "build": {"--output": {}}},
        options={"master": {}, "command": {}, "all": {}},
    )

    assert parser.last("--output", default="fallback.txt") == "fallback.txt"


def test_last_explicit_default_can_be_none():
    parser = make_parser(
        drafts={"master": {}, "build": {"--output": {"default": "result.txt"}}},
        options={"master": {}, "command": {}, "all": {}},
    )

    assert parser.last("--output", default=None) is None


def test_last_can_read_master_area():
    parser = make_parser(
        drafts={
            "master": {"--config": {}},
            "build": {},
        },
        options={
            "master": {"--config": "settings.toml"},
            "command": {},
            "all": {},
        },
    )

    assert parser.last("--config", area="master") == "settings.toml"


def test_last_with_unknown_area_returns_draft_default():
    """Current behavior: an unknown area looks like an empty options mapping."""
    parser = make_parser(
        drafts={
            "master": {},
            "build": {"--output": {"default": "result.txt"}},
        },
        options={"master": {}, "command": {}, "all": {}},
    )

    assert parser.last("--output", area="missing") == "result.txt"


def test_last_with_unknown_option_returns_none():
    parser = make_parser(
        drafts={"master": {}, "build": {}},
        options={"master": {}, "command": {}, "all": {}},
    )

    assert parser.last("--missing") is None
