
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
	# Removing your installed package using uv.
	uv pip uninstall anomlib
	uv pip uninstall fourgy


add:
	# Installing your newly uploaded package using uv.
	uv pip install anomlib
	uv pip install fourgy

reinstall: uninstall add
upgrade: upload install


guide:
	# learn how to pack with pip: https://packaging.python.org/en/latest/tutorials/packaging-projects


## System
system-require-twine:
	# Install Twine
	python3 -m pip install --upgrade twine

system-install: build
	# Installing your newly uploaded package using uv.
	python3 -m pip install anomlib==$(version)

