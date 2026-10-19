

# from pathlib import Path

# import subprocess, re
# import sys, tarfile, stat
# import hashlib, time
# import logging, os, sys

# import hashlib
# import re
# import stat
# import subprocess
# import sys
# import tarfile
# import time
import difflib
import diff_match_patch
# import difflib

# import transpkg.builtin.list
import anomlib.pillow
import anomlib.shell

# import transpkg.diffTools

# Diff Status Codes
SAME = 0
DIFFERENT = 1
TROUBLE = 2


# Note: This function is obsolete
# It cant handle comparison of huge files inside pipelines
# If you cant find diff library, store input inside files 1st and then compare them.
def shell_diff(txt, txt2, new="+ %L", old="- %L", com="  %L"):
    """
    Get Diff btw number of included files in tars.
    :param txt: Old Original Text
    :param txt2: New Updated Text
    :param new:
    :param old:
    :param com:
    """
    diff_options = [
        f'--old-line-format="{old}"',
        f'--new-line-format="{new}"',
        f'--unchanged-line-format="{com}"',
    ]

    options = " ".join(diff_options)
    command = f'echo "{txt}" | diff {options} - <(echo "{txt2}")'
    return anomlib.shell.read_command(
        command, status=[SAME, DIFFERENT]
    ).split("\n")


# def strip_file():
#     "Remove empty strings from list"
#     return [i.strip() for i in items if i.strip()]


# def strip_list(items):
#     "Remove empty strings from list"
#     return [i.strip() for i in items if i.strip()]

# Main Object for diffing and patching
dmp = diff_match_patch.diff_match_patch()

# Main object for comparing in dl_diff
dl = difflib.Differ()


def joinlines(text) -> str:
    "Concatenate list of strings into one by new lines"
    return "\n".join(text)


def splitlines(text) -> list[str]:
    "Split text by lines"
    return text.split('\n')


def dmp_diff(old, new, pkg=True) -> list[str]:
    """
    Diff two list of lines.
    Usually lines of the file before and after changes.
    :param old: Old Version of file's lines.
    :param new: New Version of file's lines.
    """
    if pkg:
        # Clean lists from empty and blank strings
        old = joinlines(old)
        new = joinlines(new)

    patches = dmp.patch_make(old, new)

    return dmp.patch_toText(patches).split("\n")


def dmp_patch(old, diffs) -> list[str]:
    """
    Patch patch in diff format to old file lines to restore new version.
    :param old: Old Version of file's lines.
    :param diffs: A patch in diff-format.
    :result list[str]: New Version of file's lines.
    """
    # Clean lists from empty and blank strings
    old = joinlines(old)

    restored_patches = dmp.patch_fromText(diffs)

    # Restore new version (by applying patch to the old version)
    new, _ = dmp.patch_apply(restored_patches, old)

    # Return File-lines of new version
    return new.split("\n")


def _filter_diff(diff: list[str], include=("+", " ", "-")) -> list[str]:
    """Filter diff to include only selected lines.

    :param _diff: list of lines in diff format
    :param include: Filter diff lines. Defaults are '+', ' ' and '='.
    """
    return [i for i in diff if i.startswith(include)]


def _censor_diff(diff: list[str], exclude="?") -> list[str]:
    """Censor diff to exclude selected lines.

    :param _diff: list of lines in diff format
    :param include: Excluding diff lines. Default one is '?'.
    """
    return [i for i in diff if not i.startswith(exclude)]


# require difflib for it
def dl_diff(old: list[str], new: list[str], ignore="?") -> list[str]:
    """Compare two packages and return list of changes in pre-adiff format.

    :param old:
    :param new:
    :param ignore: Ignore (lines,...) from diff script.
    """

    result = list(dl.compare(old, new))

    # Exclude notes on trend of changes
    # Note: we excluded lines that on '?' in diff script
    result = _censor_diff(result, ignore)

    return result


def dl_diffs(_old, patch) -> list[str]:
    """Parse two packages and return list of changes in pre-adiff format.

    :param _old: [unnecessary] old file [Keep For Compatibility]
    :param diffs: The patch we gonna use to restore new version.
    :return str: New version.
    """
    return difflib.restore(patch, 2)
    # Note: patch contains all info needed to restore both versions


a = "https://site.com/images/item-00001.png?size=large"
b = "https://site.com/images/item-00156.png?size=large"


def compare(a, b, cmp=dmp_diff):
    return cmp(a.split("/"), b.split("/"))


result = compare(a, b, cmp=dl_diff)

print(result)

c = [i for i in result if i.startswith(("-", "+"))]
assert len(c) == 2, "We don't support URLs with multiple changes"
