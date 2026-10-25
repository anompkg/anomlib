<div align="center">
    <!-- <img src="./assets/logo.svg" alt="" width="192" align="center" /> -->
    <h1 align="center">Welcome to Anomlib</h1>
</div>

## Introduction

Anomlib is a project that my key projects use.
It shares libraries such as:

- **Shell command wrapper**:
Executes shell commands from Python. Made transition easier from Bash to Python.
- **Parameter parser**:
Splits command-line arguments into logical areas.
It currently supports tool and sub-command areas.
An args-only area introduced by `--` is planned.
The nested sub-commands are not planned yet, but considered.
Parameters are defined within drafts in TOML configuration files.
- **Pillow**:
Provides hashing functions and ensures that required directories and files exist.
This library may eventually be deprecated or reduced to a hashing-only library.
- **Load**:
Compares the execution speed of compatible functions.
- **Confman**:
A simple configuration manager.
- **Cpconf**:
Copies configuration files into the user’s home configuration directory
without overwriting custom configurations that already exist.

## Legacy Bash Scripts

Anomlib also includes older Bash scripts
that are planned to be rewritten in Python over time.

- **Dowith**:
Runs command-line arguments in a loop
and supports using `readline` input as a sub-command with arguments.
- **[Picload][picload]**:
Downloads collections or albums of pictures from the internet,
such as wallpaper sets and csomics.
- **u2**:
Parses YouTube-related data. Its future purpose is not decided yet.
- **w2v** and **undub**:
Removes duplicate lines from input.
- **Whitespace**:
Removes trailing whitespace from lines.
- **Chroot into Gentoo**:
Some old Gentoo oriented scripts that you can source to simplify
entering a freshly installed Gentoo System from the TTY using `chroot`.

## Utility Scripts

Anomlib has several small Bash scripts,
that were useful on my path of learning system administration and desktop automation
and Linux in general:

- Finding commands by walking through `PATH`.
- Listing Flatpak applications, selecting one through `dmenu`, and running it.
- Working with file descriptor fd3.
- Removing noise from media files using FFmpeg.
- Making the backlight writable for Window Managers that may require it.
- Toggling warm screen lighting.
- Other small utilities for command automation, system configuration, and media processing.

Some scripts are primitive and some were lost in time and never got into git,
but they served its purpose at certain point.

## Shared uv Makefile

Anomlib provides a common `uv.mk` Makefile for use across my projects.
The `uv.mk` file is maintained and updated here.
It helps build/clean/update venv, push to/fetch from PyPI.

Copy the `Makefile` into your project and modify it to suit that project’s requirements.
Do not delete it, as it contains personal requirements shared across your projects.
You will usually need to update the `deps` and `work` variables.

The `Makefile` can download `uv.mk` automatically.
If your local `uv.mk` file is outdated, remove it and run the `Makefile` again
    to download the latest version.
You can also customize the `download-uv-mk` target
    to download `uv.mk` from a different URL.

## Planned Framework (Ifuse)

I plan to create my first small framework (ifuse)
by combining some of my shared libraries into a single entity.
It will provide access to configuration files,
environment variables, and command-line parameters.

Ifuse may also support an interactive mode using `readline`.
Optionally, it could provide an interactive background API service
for controlling the application through API requests.
We also may also allow binding some OS signals to events.

Ifuse may be somewhat similar to `confuse`, although that was not intentional.
The original goal was simply to create my first small framework.
The framework has staged processing of input channels,
while both original input and processed will remain accessible.
Main idea is to merge all channels into one settings object,
and let all input sources simple to access and control over app.

## Learn Markdown Notes

To lean how to write Markdown, you can check
[GitHub-flavored Markdown](https://guides.github.com/features/mastering-markdown/)
guide.

[picload]: doc/Picload.md