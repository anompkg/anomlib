"Library wrapped around yt-dlp"

from pathlib import Path
import sys,os

import anomlib.shell
import anomlib.pillow


# You can group videos by categories. e.g. Linux, NSFW, Memes, Movies, Music, How2 etc. 
# by default videos are stored in Unknown group.
# Feel free to move it into another group manually.
group = "Unknown/%(channel_id)s"
output = "%(title)s [%(id)s].%(ext)s".

home = Path.home()

# anomtool-youtube's home directory
youtube = home / "Videos/Youtube/ytool"
# Ytool is a command that is wrapped around anomtool-youtube builtin command
videos = youtube / group

video = videos / output

## how to use manually:
# >>> print(f"{dest}/{output}" % {'title': "a", 'id': "b", 'ext': "c"})
# >>> str(video) % {'title':'video','id':'1','ext':'mp4'}
# Note: check 'man yt-dlp' to know more about "available fields".

pillow.mkdirs(videos)

# Current youtube-dl tool
yt_dl = "yt-dlp"

def yt(args=[], options='--all-subs'):
    f"{yt_dl} {options} -- {' '.join(args)}"

yt(sys.argv[1:])

