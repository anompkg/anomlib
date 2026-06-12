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

uninstall:
	# Removing old versions
	uv pip uninstall anomlib
	uv pip uninstall transpkg

add:
	# Installing your newly uploaded package using uv.
	uv pip install anomlib
	uv pip install transpkg

upgrade: upload install
reinstall: uninstall add

guide:
	# learn how to pack with pip: https://packaging.python.org/en/latest/tutorials/packaging-projects


## System
system-require-twine:
	# Globally Install Twine
	python3 -m pip install --upgrade twine

system-install: build
	# Globally install your newly uploaded package using pip.
	python3 -m pip install anomlib==$(version)

