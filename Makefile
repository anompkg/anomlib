install:
	@# Install commands in local directory
	@cp -r bin/*[^~] $(HOME)/.local/bin/


sudo-install:
	@# Install commands in the root /bin directory
	@sudo cp bin/*[^~] /bin/

