default: install

install:
	# Install cmds at ~/.local/bin folder
	@ cp -r bin/*[^~] $(HOME)/.local/bin/
	# Done.


sudo-install:
	# Install cmds at /bin folder
	@ sudo cp bin/*[^~] /bin/
	# Done.

