version = $(shell uv version --short)
name = $(shell uv version | sed "s/ .*//")


# Paths to pips to select from
# VS-code looks here
pipg = /home/neon/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/bin/pip
pipg_options = --break-system-packages
pipx = pipx
pip = uv pip

# Default pip
PIP ?= pip

# Select pip
piper ?= $(pip_prefix) $($(PIP))
PIP_options ?= $($(PIP)_options)

version:
	@echo version: $(version)
	@echo name: $(name)
	@echo deps: $(deps)
	@echo workspace: $(work)
	@echo pip: $(piper)
	@echo pip options: $(PIP_options)

default: install
	# Installing anomlib by default

buildtest: tests build

build: add clean
	# Build Anomlib Package
	uv build

venv:
	# Making sure venv is created
	@ [[ -d .venv ]] || uv venv

install:
	# Install Requirements like Twine
	# Installing your newly uploaded package using uv.
	# Note: If you cant get fresher versions do `make gc'
	$(piper) install $(PIP_options) --upgrade $(work)

uninstall: venv
	# Remove Requirements like Twine
	$(piper) uninstall $(PIP_options) $(work)

add: venv
	# Update Dependencies
	uv add $(deps)

remove: venv
	# Remove Dependencies
	uv remove $(deps)


upload: install
	# Upload Packages
	uv run twine upload dist/* --verbose

clean: gc
	# Cleaning build's cache artifacts...
	rm -r dist/ src/$(name).egg-info ||:
	# Clean anomlib library
	rm -r '.venv/lib/python3.12/site-packages/anomlib'* ||:

gc:
	# Cleaning uv pre-built cache artifacts...
	uv clean

self: venv
	$(piper) install $(PIP_options) .

readd: remove add
reinstall: uninstall install
upgrade: readd upload reinstall


.PHONY: tests
tests:
	# Run PyTests
	uv run pytest -rxa package
	uv run pytest -rxa tests
#	python -m unittest discover src/transpkg/tests
#	# or
#	#python -m unittest discover -s <directory> -p '*_test.py'

guide:
	# learn how to pack with pip: https://packaging.python.org/en/latest/tutorials/packaging-projects

