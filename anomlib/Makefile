version = $(shell uv version --short)

version:
	echo version: $(version)

default: install
	# Installing anomlib by default

build: venv clean
	# Build Anomlib Package
	uv build

venv:
	# Making sure venv is created
	@ [[ -d .venv ]] || uv venv

require-twine: build
	# Install Twine
	uv pip install --upgrade twine

upload: require-twine
	# Upload Packages
	@uv run python3 -m twine upload dist/* --verbose

clean:
	# Cleaning build's cache artifacts...
	@rm -r dist/ src/anomlib.egg-info ||:

gc:
	# Cleaning uv pre-built cache artifacts...
	uv clean

uninstall:
	# Removing old versions
	uv pip uninstall anomlib

add:
	# Installing your newly uploaded package using uv.
	# Note: If you cant get fresher versions do `make gc'
	uv pip install anomlib

install: gc add
reinstall: uninstall install
upgrade: upload reinstall

guide:
	# learn how to pack with pip: https://packaging.python.org/en/latest/tutorials/packaging-projects


## System
system-require-twine:
	# Globally Install Twine
	python3 -m pip install --upgrade twine

system-install: build
	# Globally install your newly uploaded package using pip.
	python3 -m pip install anomlib==$(version)

