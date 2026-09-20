<!-- <div align="center">
    <img src="./assets/logo.svg" alt="" width="192" align="center" /> -->
<h1 align="center">Welcome to Anomlib</h1>
<!-- </div> -->

This project contains shared libraries that my key projects use:

- **Shell command wrapper** — Executes shell commands from Python. Made transition easier from Bash to Python.
- **Parameter parser** — Splits command-line arguments into logical areas. It currently supports tool and subcommand areas. An args-only area introduced by `--` is planned, and nested subcommands may be supported in the future. Parameters are defined within drafts in TOML configuration files.
- **Pillow** — Provides hashing functions and ensures that required directories and files exist. This library may eventually be deprecated or reduced to a hashing-only library.
- **Load** — Compares the execution speed of compatible functions.
- **Confman** — A simple configuration manager.
- **Cpconf** — Copies configuration files into the user’s home configuration directory without overwriting custom configurations that already exist.

## Legacy Bash Scripts

This project also includes older Bash scripts that are planned to be rewritten in Python over time.

- **Dowith** — Runs command-line arguments in a loop and supports using `readline` input as a subcommand with arguments.
- **Picloads** — Helps organize collections or albums of pictures from the internet, such as wallpaper sets.
- **U2** — Parses YouTube-related data. Its future purpose is still undecided.
- **W2v** — Removes duplicate lines from input.
- **Whitespace** — Removes trailing whitespace from lines.
- **Gentoo utilities** — Includes older Gentoo-oriented scripts that can be sourced to simplify entering a freshly installed Gentoo system from a TTY using `chroot`.

## Utility Scripts

This project includes several small Bash scripts for everyday system administration and desktop automation, including:

- Finding commands by walking through `PATH`.
- Listing Flatpak applications, selecting one through `dmenu`, and running it.
- Working with file descriptor 3.
- Removing noise from media files using FFmpeg.
- Making the backlight writable for window managers that require it.
- Toggling warm screen lighting.
- Other small utilities for command automation, system configuration, and media processing.

## Shared uv Makefile

This project provides a common `uv.mk` Makefile for use across my projects. The `uv.mk` file is maintained and updated here.

Copy the `Makefile` into your project and modify it to suit that project’s requirements. Do not delete it, as it contains personal requirements shared across your projects. You will usually need to update the `deps` and `work` variables.

The `Makefile` can download `uv.mk` automatically. If your local `uv.mk` file is outdated, remove it and run the `Makefile` again to download the latest version. You can also customize the `download-uv-mk` target to download `uv.mk` from a different URL.

## Planned Framework

I plan to create my first small framework by combining some of my shared libraries into a single entity. It will provide access to configuration files, environment variables, and command-line parameters.

The framework may also support an interactive mode using `readline`. Optionally, it could provide an interactive background API service for controlling the application through API requests. It may also handle operating-system signals and convert them into application events.

The framework may be somewhat similar to `confine`, although that was not intentional. The original goal was simply to create my first small framework.