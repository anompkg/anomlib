#!/usr/bin/env python3

"""
Copy Default configs. Skip custom configs.
"""

from argparse import Namespace
from __future__ import annotations

import argparse
import shutil
import sys
import pathlib
from pathlib import Path


# Note: you can take .. from directory via parent:
# CONF = Path(__file__).parent.parent / "src/anomlib/conf"
# It works different in case with ./README.md/.., or .parent with dirname()
# Shell does not allow /.. after filename, but it would equivalent to dirname() 

# Path to Configs inside git project
CONF = Path(__file__) / "../../src/anomlib/conf"

# Copy into ~/.config/anomlib/
DEST = Path.home() / ".config/anomlib"


def mkdirs(path):
    "Make directory and all its parent dirs exist"
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)


def install_configs(source_dir: Path, overwrite: bool, dry_run: bool) -> None:
    config_dir = DEST

    mkdirs(config_dir)
    if not source_dir.is_dir():
        raise SystemExit(f"Source directory does not exist: {source_dir}")

    # Walk all local/source configs
    for source_path in source_dir.rglob("*"):
        if not source_path.is_file():
            continue

        relative_path = source_path.relative_to(source_dir)
        destination_path = config_dir / relative_path

        if destination_path.exists() and not overwrite:
            print(f"skip     {destination_path}")
            continue

        print(
            f"{'overwrite' if destination_path.exists() else 'install'} "
            f"{destination_path}"
        )

        if dry_run:
            continue

        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, destination_path)


def parse_args():
    "Parse "
    parser = argparse.ArgumentParser(
        description="Install configuration files into ~/.config"
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=CONF,
        help="Directory containing configuration files",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite files that already exist",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would happen without copying files",
    )

    return parser.parse_args()


def make_configs():
    """Make sure configs exist.
    Copy over default configs if there are no configs yet"""

    args = parse_args()

    try:
        mkdirs(args.source.expanduser().resolve())
        install_configs(
            source_dir=args.source.expanduser().resolve(),
            overwrite=args.overwrite,
            dry_run=args.dry_run,
        )
    except OSError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    return 0
