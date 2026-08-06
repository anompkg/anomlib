version = $(shell uv version --short)
name = $(shell uv version | sed "s/ .*//")

version:
	echo version: $(version)
	echo name: $(name)
	echo foo: $(foo)

default: install
	# Installing anomlib by default

build: venv clean
	# Build Anomlib Package
	uv build

venv:
	# Making sure venv is created
	@ [[ -d .venv ]] || uv venv

install: build
	# Install Requirements like Twine
	# Installing your newly uploaded package using uv.
	# Note: If you cant get fresher versions do `make gc'
	uv pip install --upgrade $(work)

uninstall: venv
	# Remove Requirements like Twine
	uv pip uninstall $(work)

add: venv
	# Update Dependencies
	uv add $(deps)

remove: venv
	# Remove Dependencies
	uv remove $(deps)


upload: install
	# Upload Packages
	@uv run python3 -m twine upload dist/* --verbose

clean: gc
	# Cleaning build's cache artifacts...
	rm -r dist/ src/$(name).egg-info ||:
	# Clean anomlib library
	rm -r '.venv/lib/python3.12/site-packages/anomlib'* ||:

gc:
	# Cleaning uv pre-built cache artifacts...
	uv clean

self: venv
	uv pip install .

readd: remove add
reinstall: uninstall install
upgrade: upload reinstall


tests:
	# Run PyTests
	uv run pytest src/$(name)/tests
#	uv run pytest
#	python -m unittest discover src/transpkg/tests
#	# or
#	#python -m unittest discover -s <directory> -p '*_test.py'

guide:
	# learn how to pack with pip: https://packaging.python.org/en/latest/tutorials/packaging-projects

