# About Dowith

Run commands in `pseudo-interactive` mode.
Arguments given into `dowith` are treated as `interpreter`.
`Note:` each line is being run `separately`
and there is `no such thing` as a single session.

`Note:` Arguments given into `dowith` may be called a `base`, `interpreter` or `runner`.

## Default Commands

`break` and `exit` - stop `runner` cycle and exit

`Note:` In the future, For exit Ctrl-D is also planned.

## Examples

```bash
# Run binary commands only
dowith command

# Run git pseudo-interactively
dowith git
# >>> status
# runs: git status

## Emulate shell inside shell
dowith eval
# We Use `eval` command as a `base runner`

# You can Fetch videos, pages interactively:
dowith youtube-dl --  # Download video from YouTube
dowith yt-dlp --  # Download video from YouTube
dowith curl -- # Download image/page from Internet
dowith wget -- # Download image/page from Internet

# Run some commands from swayconfig interactively
dowith swaymsg

# Run some commands from i3config interactively
dowith i3-msg

```
