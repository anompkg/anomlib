#!/home/neon/.local/share/uv/tools/teslar/bin/python
# -*- coding: utf-8 -*-

import sys
from teslar.commands.teslar import main

SCRIPT_EXTENSIONS = ("-script.pyw", ".exe")


# My updated function
def _strip_script_extension(script, extensions=SCRIPT_EXTENSIONS):
    "Transform and return script-name with fixed extension"
    for extension in extensions:
        if script.endswith(extension):
            return script[:-len(extension)]
    return script


# My updated function
def strip_script_extension():
    sys.argv[0] = _strip_script_extension(sys.argv[0])


if __name__ == "__main__":
    strip_script_extension()
    sys.exit(main())
    # or
    # raise SystemExit(main())
