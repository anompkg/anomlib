# Include shared uv Makefile

# Dependencies
deps ?= pytest twine $(pkgs)
# Working packages, including current project
work ?= anomlib $(deps)

default-command: uv.mk
	# Make sure uv is installed.

.PHONY: uv.mk
uv.mk:
	# Require uv.mk Makefile
	@[[ -f uv.mk ]] || make download-uv.mk

download-uv.mk:
	# Download uv.mk
	@wget 'https://codeberg.org/anom/anomlib/raw/branch/master/anomlib/uv.mk'

# Optionally require uv.mk
# If it is missing run `make` to download
-include uv.mk

