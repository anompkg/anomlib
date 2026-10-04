default: install

.PHONY: check install default sudo-install

install:
	# Install cmds at ~/.local/bin folder
	@ cp -r bin/*[^~] $(HOME)/.local/bin/
	# Done.


sudo-install:
	# Install cmds at /bin folder
	@ sudo cp bin/*[^~] /bin/
	# Done.

check:
	@set -eu; \
	for src in bin/*; do \
		[ -f "$$src" ] || continue; \
		name=$${src##*/}; \
		dst="$$HOME/.local/bin//$$name"; \
		if [ ! -f "$$dst" ] || ! cmp -s "$$src" "$$dst"; then \
			printf '%s\n' "$$name"; \
		fi; \
	done
