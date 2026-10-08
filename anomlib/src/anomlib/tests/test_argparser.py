import argparse

import pytest
import tomlkit

from anomlib import argparser as sut


def make_drafts(options=None, *, command="run"):
    return {
        command: options or {},
    }


# --- to_python() ---


def test_to_python_recursively_converts_toml_document():
    document = tomlkit.parse(
        """
        [run]
        name = "example"
        enabled = true
        values = [1, 2, 3]

        [run.nested]
        key = "value"
        """
    )

    result = sut.to_python(document)

    assert result == {
        "run": {
            "name": "example",
            "enabled": True,
            "values": [1, 2, 3],
            "nested": {"key": "value"},
        }
    }
    assert isinstance(result, dict)
    assert isinstance(result["run"]["values"], list)


def test_to_python_converts_tuples_to_lists():
    assert sut.to_python((1, {"value": 2})) == [1, {"value": 2}]


def test_to_python_leaves_plain_values_unchanged():
    for value in (None, True, 3, 2.5, "text"):
        assert sut.to_python(value) == value


# --- copy_dict() ---


def test_copy_dict_is_a_deep_copy():
    original = {"nested": {"items": [1, 2]}}
    copied = sut.copy_dict(original)

    copied["nested"]["items"].append(3)

    assert original == {"nested": {"items": [1, 2]}}
    assert copied == {"nested": {"items": [1, 2, 3]}}


# --- Parser construction and draft handling ---


def test_default_drafts_include_diff_command():
    parser = sut.ArgParser("diff")

    assert parser.command == "diff"
    assert "patch" in parser.params
    assert "output" in parser.params
    assert "args" in parser.params


def test_unknown_command_raises_value_error(capsys):
    with pytest.raises(ValueError, match="Unknown command"):
        sut.ArgParser("not-a-command", drafts={"run": {}})

    # Current implementation prints the drafts before raising.
    assert "{'run': {}}" in capsys.readouterr().out


def test_build_adds_default_positional_argument():
    parser = sut.ArgParser("run", drafts={"run": {}})

    result = parser.parse_args([])

    assert result["args"] == []


def test_empty_draft_mapping_is_accepted():
    parser = sut.ArgParser("run", drafts={"run": {}})

    assert parser.parse_args([])["args"] == []


# --- Value options ---


def test_value_option_accepts_long_and_short_aliases():
    parser = sut.ArgParser(
        "run",
        drafts=make_drafts({
            "output": {
                "class": "value",
                "shorts": "o",
                "type": "string",
            }
        }),
    )

    assert parser.parse_args(["--output", "first.txt"])["output"] == ["first.txt"]
    assert parser.parse_args(["-o", "second.txt"])["output"] == ["second.txt"]


def test_value_option_accepts_keys_as_long_aliases():
    parser = sut.ArgParser(
        "run",
        drafts=make_drafts({
            "output": {
                "class": "value",
                "keys": ["file"],
                "type": "string",
            }
        }),
    )

    assert parser.parse_args(["--file", "result.txt"])["output"] == ["result.txt"]


def test_value_option_defaults_to_empty_list():
    parser = sut.ArgParser(
        "run",
        drafts=make_drafts({
            "output": {"class": "value", "type": "string"},
        }),
    )

    assert parser.parse_args([])["output"] == []


@pytest.mark.parametrize(
    ("type_name", "argument", "expected"),
    [
        ("string", "abc", "abc"),
        ("int", "42", 42),
        ("integer", "42", 42),
        ("float", "2.5", 2.5),
    ],
)
def test_value_option_converts_supported_types(type_name, argument, expected):
    parser = sut.ArgParser(
        "run",
        drafts=make_drafts({
            "value": {"class": "value", "type": type_name},
        }),
    )

    assert parser.parse_args(["--value", argument])["value"] == [expected]


def test_value_option_rejects_unsupported_type():
    with pytest.raises(ValueError, match="Unsupported option type"):
        sut.ArgParser(
            "run",
            drafts=make_drafts({
                "value": {"class": "value", "type": "decimal"},
            }),
        )


# --- Flags ---


def test_flag_can_be_enabled_by_long_option():
    parser = sut.ArgParser(
        "run",
        drafts=make_drafts({
            "verbose": {"class": "flag"},
        }),
    )

    assert parser.parse_args(["--verbose"])["verbose"] == 1


def test_flag_can_be_enabled_by_short_option():
    parser = sut.ArgParser(
        "run",
        drafts=make_drafts({
            "verbose": {
                "class": "flag",
                "shorts": "v",
            },
        }),
    )

    assert parser.parse_args(["-v"])["verbose"] == 1


def test_flag_short_string_creates_multiple_short_options():
    parser = sut.ArgParser(
        "run",
        drafts=make_drafts({
            "patch": {
                "class": "flag",
                "shorts": "pu",
            },
        }),
    )

    assert parser.parse_args(["-p"])["patch"] == 1
    assert parser.parse_args(["-u"])["patch"] == 1


def test_flag_can_be_enabled_with_key_alias():
    parser = sut.ArgParser(
        "run",
        drafts=make_drafts({
            "verbose": {
                "class": "flag",
                "keys": ["verbosity"],
            },
        }),
    )

    assert parser.parse_args(["--verbosity"])["verbose"] == 1


def test_flag_count_increments_when_repeated():
    parser = sut.ArgParser(
        "run",
        drafts=make_drafts({
            "verbose": {"class": "flag"},
        }),
    )

    assert parser.parse_args(["--verbose", "--verbose"])["verbose"] == 2


def test_negative_flag_aliases_set_false():
    parser = sut.ArgParser(
        "run",
        drafts=make_drafts({
            "patch": {"class": "flag"},
        }),
    )

    assert parser.parse_args(["--no-patch"])["patch"] is False
    assert parser.parse_args(["--non-patch"])["patch"] is False


def test_negative_flag_after_positive_flag_sets_false():
    parser = sut.ArgParser(
        "run",
        drafts=make_drafts({
            "patch": {"class": "flag"},
        }),
    )

    assert parser.parse_args(["--patch", "--no-patch"])["patch"] is False


def test_positive_flag_after_negative_flag_starts_counting():
    parser = sut.ArgParser(
        "run",
        drafts=make_drafts({
            "patch": {"class": "flag"},
        }),
    )

    assert parser.parse_args(["--no-patch", "--patch"])["patch"] == 1


@pytest.mark.xfail(
    strict=False,
    reason="bool is registered as bool; bool('false') evaluates to True.",
)
def test_bool_value_type_parses_false_text_as_false():
    parser = sut.ArgParser(
        "run",
        drafts=make_drafts({
            "enabled": {"class": "value", "type": "bool"},
        }),
    )

    assert parser.parse_args(["--enabled", "false"])["enabled"] == [False]


# --- Positional arguments and intermixed parsing ---


def test_positional_arguments_are_collected():
    parser = sut.ArgParser("run", drafts={"run": {}})

    assert parser.parse_args(["one.txt", "two.txt"])["args"] == [
        "one.txt",
        "two.txt",
    ]


def test_positional_arguments_can_be_interspersed_with_options():
    parser = sut.ArgParser(
        "run",
        drafts=make_drafts({
            "output": {"class": "value", "type": "string"},
        }),
    )

    result = parser.parse_args(
        ["before.txt", "--output", "result.txt", "after.txt"]
    )

    assert result["args"] == ["before.txt", "after.txt"]
    assert result["output"] == ["result.txt"]


# --- Validation and dispatch ---


def test_unsupported_option_class_raises_value_error():
    with pytest.raises(ValueError, match="Unsupported option class"):
        sut.ArgParser(
            "run",
            drafts=make_drafts({
                "value": {"class": "mystery"},
            }),
        )


def test_missing_class_defaults_to_value():
    parser = sut.ArgParser(
        "run",
        drafts=make_drafts({
            "output": {"type": "string"},
        }),
    )

    assert parser.parse_args(["--output", "out.txt"])["output"] == ["out.txt"]


def test_add_arg_ignores_option_alias_fields():
    parser = sut.ArgParser(
        "run",
        drafts=make_drafts({
            "files": {
                "class": "arg",
                "nargs": "*",
                "shorts": "f",
                "keys": ["file"],
            }
        }),
    )

    assert parser.parse_args(["a.txt", "b.txt"])["files"] == [
        "a.txt",
        "b.txt",
    ]


# --- Parser injection and argument merging ---


def test_custom_parser_is_used():
    custom_parser = argparse.ArgumentParser(prog="custom")

    parser = sut.ArgParser(
        "run",
        drafts={"run": {}},
        parser=custom_parser,
    )

    assert parser.parser is custom_parser
    assert parser.parser.prog == "custom"


def test_merge_parser_arguments_adds_missing_argument():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--verbose", action="count", default=0)

    target = sut.ArgParser("run", drafts={"run": {}})
    target.merge_parser_arguments(parser)

    assert target.parse_args(["--verbose"])["verbose"] == 1


def test_merge_parser_arguments_does_not_replace_existing_destination():
    source = argparse.ArgumentParser(add_help=False)
    source.add_argument("--output", dest="output", default="source")

    target = sut.ArgParser(
        "run",
        drafts=make_drafts({
            "output": {"class": "value", "type": "string"},
        }),
    )
    target.merge_parser_arguments(source)

    result = target.parse_args(["--output", "target"])

    assert result["output"] == ["target"]


def test_merge_parser_arguments_skips_help_action():
    source = argparse.ArgumentParser()
    target = sut.ArgParser("run", drafts={"run": {}})

    target.merge_parser_arguments(source)

    assert sum(
        action.dest == "help"
        for action in target.parser._actions
    ) == 1


def test_merge_parser_arguments_skips_option_string_collision():
    source = argparse.ArgumentParser(add_help=False)
    source.add_argument("-v", dest="source_verbose", action="store_true")

    target = sut.ArgParser(
        "run",
        drafts=make_drafts({
            "verbose": {
                "class": "flag",
                "shorts": "v",
            }
        }),
    )

    # The source action has a different destination but collides on "-v".
    target.merge_parser_arguments(source)

    assert target.parse_args(["-v"])["verbose"] == 1
