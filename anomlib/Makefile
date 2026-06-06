default: install
	# Installing anomlib by default

build: venv clean
	# Build Anomlib Package
	uv build

venv:
	# Make sure venv is created
	[[ -d .venv ]] || uv venv

require-twine: build
	# Install Twine
	uv pip install --upgrade twine

upload: build require-twine
	# Upload Packages
	uv run python3 -m twine upload --repository testpypi dist/* --verbose

clean:
	uv clean
	# Clean build's cache artifacts
	rm -r dist/ src/anomlib_package_transpkg.egg-info

install: build
	# Installing your newly uploaded package using uv.
	uv pip install --index-url https://test.pypi.org/simple/ --no-deps anomlib-package-transpkg

uninstall:
	# Removing your installed package using uv.
	uv pip uninstall anomlib-package-transpkg

guide:
	# learn how to pack with pip: https://packaging.python.org/en/latest/tutorials/packaging-projects
