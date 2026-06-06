build:
	# Build Anomlib Package
	@python3 -m build

upload: build
	# Install Twine
	python3 -m pip install --upgrade twine
	# Upload Packages
	python3 -m twine upload --repository testpypi dist/*
install:
	# Installing your newly uploaded package
	python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps anomlib-package-transpkg
guide:
	# learn how to pack with pip: https://packaging.python.org/en/latest/tutorials/packaging-projects
